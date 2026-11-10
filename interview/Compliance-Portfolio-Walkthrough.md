# Five-Minute CISO Assistant Walkthrough

## 1. ISO 27001 — 90 seconds

Open **Audits → ISO 27001 SoA — CloudNative Analytics**. Show A.8.1, A.5.23 and one physical exclusion. Explain the business facts, linked risk, evidence gap and why a completed review is not a compliance claim.

## 2. EU AI Act / AI governance — 90 seconds

Open **EU AI Act High-Risk Assessment — TalentMatch**. Show Article 14.1, then **Action plan** for PROP-AI-R003. Explain how the top-20 workflow can make human review symbolic. Then open the NIST and ISO crosswalk audits to show governance traceability.

## 3. SOC 2 — 60 seconds

Open **SOC 2 Readiness Assessment — CloudNative Analytics** and expand CC6 and CC8. Explain that AWS-only infrastructure and managed laptops make access and change management relevant, while no operating evidence was supplied; therefore the result remains Not assessed.

## 4. PCI DSS — 60 seconds

Open **PCI DSS Network Segmentation and Scope Assessment**. Show 1.2.4, 1.4.1 and 11.4.5. Explain that a CDE box in a network diagram is not proof of segmentation: AD, jump host, SIEM, backup and WSUS can expand scope.

## Interview rule

Always separate: **what the scenario proves**, **what remains unverified**, **the risk created**, and **the evidence required to close the finding**. Do not claim certification, an approved risk acceptance, technical testing, or live-system verification.

## 5. FinanceFlow risk acceptance — 60 seconds

Open **Risk → PaymentReconciler v3.2 Shared DBA Account Risk Assessment**, then show `RA-2026-017`. Explain the business risk in plain language: 15 people know an unrotated administrator password for a PCI database handling $2B in annual transactions, and query activity cannot be reliably reconstructed. Show the vulnerability record and the pending Governance → Risk acceptances request. State that the CFO is the proposed owner, not an approver yet. Demonstrate the conditions—rotation, named minimum access, monitoring, IP restrictions and funded replacement—and explain that residual risk cannot be treated as low until evidence exists.
