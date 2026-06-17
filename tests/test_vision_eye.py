import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viki.vision import VisualAudit

eye = VisualAudit()

print("\n======================================================")
print("VISION SIMULATION: LAYOUT INTEGRITY CHECK")
print("======================================================\n")

# Сценарий: Агент сверстал PDF, но логотип перекрыл текст (Visual Discrepancy)
print(">>> STEP 1: Agent reports PDF generation successful.")
image_mock = "generated_invoice.png"
blueprint = "Check for logo overlap and font consistency."

print("\n[V.I.K.I. EXECUTION BOUNDARY] Running Visual Audit...")
is_ok, msg = eye.verify_layout(image_mock, "CRITICAL: Detected overlap on Page 1")

if not is_ok:
    print(f"❌ {msg}")
    print(">>> 🛑 CASCADE PREVENTED. User will not see the corrupted file. <<<")
else:
    print(f"✅ {msg}")
