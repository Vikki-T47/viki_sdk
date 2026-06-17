import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from viki.telemetry import VIKI_Telemetry
from viki.compliance import ComplianceOfficer

tel = VIKI_Telemetry()
vcr = ComplianceOfficer()

print("\n======================================================")
print("ENTERPRISE SIMULATION: AUTOMATED BANKING AUDIT")
print("======================================================\n")

tel.log_incident("SRC_GUARD", "BUDGET_OVERFLOW", {"action": "TRANSFER", "amount_usd": 50000})
tel.log_incident("VRI_INTERRUPT", "TTL_EXPIRED", {"action": "EXECUTE_ORDER", "token": "tx_998"})
tel.log_incident("PRA_AUDIT", "TOTAL_BUDGET_VIOLATION", {"plan_total": 1200})

print("\n[V.I.K.I. VCR] Generating Compliance Protocol for Legal Department...")
final_report = vcr.generate_full_audit_report()

print("\n--- OFFICIAL AUDIT TRAIL ---")
print(final_report)
print("----------------------------")
print("\n✅ AUDIT COMPLETE. Protocol ready for archival.")
