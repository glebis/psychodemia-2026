# Reconstruction & Re-identification — what survives anonymization

Default stack under test: **natasha+regex+ollama** (the RU benchmark default).
Method follows the re-identification / inference-attack literature (Staab et al.; RAT-Bench; Tau-Eval privacy–utility).

## A. Quasi-identifier survival (the re-identification surface)

An entity *survives* if **any** of its mentions is left unmasked. Direct identifiers (name/phone/email) are well masked; the danger is the quasi-identifiers that, combined, still single out a person.

| Client | Quasi-entities | Survived | Survival rate | Surviving types |
|---|--:|--:|--:|---|
| a | 10 | 2 | **20%** | MEDICATION, PROFESSION |
| b | 13 | 4 | **31%** | AGE, DATE, MEDICATION, PROFESSION |

## B. LLM inference attack on the *redacted* text

A local qwen model, given only the anonymized transcript (`<TAGS>` in place of PII), is asked to infer the client's attributes from remaining context.
Recovered = attribute correctly reconstructed despite redaction.

| Client | Recovered / tested | Reconstructed attributes |
|---|--:|---|
| a | 1/5 | medication |
| b | 0/5 | — |

_Even a 3B local model reconstructs identity-narrowing attributes from context alone; a frontier model would recover more (the literature reports state-of-the-art tools prevent re-identification only ~27–29% of the time). Redaction of direct identifiers is necessary but not sufficient._

## C. Utility cost (over-redaction)

Under the default stack, **55 of 205** redacted spans (**27%**) were not gold PII — the readability price paid for recall. In de-id this is the cheap error (over-redaction costs readability; a miss leaks PII).

