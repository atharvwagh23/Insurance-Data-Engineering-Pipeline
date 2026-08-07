import os
import pandas as pd
from utils import build_file_path
PREPROCESSED_FOLDER = "data\\preprocessed"
CURATED_FOLDER = "data\\curated"
SEMANTIC_FOLDER = "data\\semantic"
def build_curated_and_semantic():
    print("\nBuilding Curated Layer...")
    claims = pd.read_parquet(build_file_path(PREPROCESSED_FOLDER, "claims_yyyymmdd.parquet"))
    policies = pd.read_parquet(build_file_path(PREPROCESSED_FOLDER, "policies_yyyymmdd.parquet"))
    customers = pd.read_parquet(build_file_path(PREPROCESSED_FOLDER, "customers_yyyymmdd.parquet"))
    payments = pd.read_parquet(build_file_path(PREPROCESSED_FOLDER, "payments_yyyymmdd.parquet"))
    audit_cols = ["ingestion_date", "file_date"]
    policies = policies.drop(columns=audit_cols)
    customers = customers.drop(columns=audit_cols)
    payments = payments.drop(columns=audit_cols)
    curated = claims.merge(policies, on="Policy_ID", how="left")
    curated = curated.merge(customers, on="Customer_ID", how="left")
    curated = curated.merge(payments, on="Policy_ID", how="left")
    curated = curated.drop_duplicates()
    curated_output = build_file_path(CURATED_FOLDER, "curated_enriched.parquet")

    if os.path.exists(curated_output):
        existing = pd.read_parquet(curated_output)
        curated = pd.concat([existing, curated], ignore_index=True)
        curated = curated.drop_duplicates()
    curated.to_parquet(curated_output, index=False)
    print("Curated Layer Created: " + curated_output)
    print("\nBuilding Semantic Layer...")
    policy_type_agg = (
        curated.groupby("Policy_Type")
        .agg(
            Total_Claims_Amount=("Claim_Amount", "sum"),
            Claims_Count=("Claim_ID", "count")
        )
        .reset_index()
    )
    city_agg = (
        curated.groupby("City")
        .agg(
            Avg_Claim_Amount=("Claim_Amount", "mean"),
            Claims_Count=("Claim_ID", "count")
        )
        .reset_index()
    )
    policy_agg_path = build_file_path(SEMANTIC_FOLDER, "PolicyTypeAgg.parquet")
    city_agg_path = build_file_path(SEMANTIC_FOLDER, "CitiesTotalClaim.parquet")
    if os.path.exists(policy_agg_path):
        existing_policy = pd.read_parquet(policy_agg_path)
        policy_type_agg = pd.concat([existing_policy, policy_type_agg], ignore_index=True)
        policy_type_agg = policy_type_agg.drop_duplicates()
    if os.path.exists(city_agg_path):
        existing_city = pd.read_parquet(city_agg_path)
        city_agg = pd.concat([existing_city, city_agg], ignore_index=True)
        city_agg = city_agg.drop_duplicates()
    policy_type_agg.to_parquet(policy_agg_path, index=False)
    city_agg.to_parquet(city_agg_path, index=False)
    print("Semantic Layer Created:")
    print("  " + policy_agg_path)
    print("  " + city_agg_path)