"""
Rule-Based Expert System - Symptom Checker
--------------------------------------------
Syntecxhub AI Internship - Week 1, Project 2

This program is a simplified "expert system" - a type of AI that mimics
how a human expert reasons using IF-THEN rules.

How it works (in plain English):
1. We store a list of RULES. Each rule says:
   "IF the user has these symptoms, THEN they might have this condition."
2. We ask the user which symptoms they have. These become our FACTS.
3. We use FORWARD CHAINING: we check every rule against the facts we know.
   If a rule's conditions are fully satisfied by our facts, we "fire" it -
   meaning we accept its conclusion as a new fact.
4. Some conclusions can trigger OTHER rules too (multi-step / chained
   inference) - e.g. "if you have a common cold AND a fever, you may need
   to see a doctor."
5. We keep a LOG of every step so the user can see exactly how the system
   reasoned its way to the final answer (this is what makes it "explainable AI").
"""

# ---------------------------------------------------------
# STEP 1: Define the knowledge base (the rules)
# ---------------------------------------------------------
# Each rule is a dictionary with:
#   "if"   -> a list of facts/symptoms that must ALL be true
#   "then" -> the new fact/conclusion to add if the rule fires
#   "name" -> a label used only for the reasoning log
RULES = [
    {
        "name": "Rule 1",
        "if": ["cough", "sore_throat"],
        "then": "common_cold"
    },
    {
        "name": "Rule 2",
        "if": ["fever", "body_ache", "fatigue"],
        "then": "flu"
    },
    {
        "name": "Rule 3",
        "if": ["fever", "cough", "shortness_of_breath"],
        "then": "possible_respiratory_infection"
    },
    {
        "name": "Rule 4",
        "if": ["sneezing", "itchy_eyes", "runny_nose"],
        "then": "allergy"
    },
    {
        "name": "Rule 5 (chained)",
        "if": ["common_cold", "fever"],
        "then": "see_a_doctor"
    },
    {
        "name": "Rule 6 (chained)",
        "if": ["flu", "shortness_of_breath"],
        "then": "seek_urgent_care"
    },
]

# Friendly messages for each conclusion, shown at the end
CONCLUSION_MESSAGES = {
    "common_cold": "You may have a Common Cold.",
    "flu": "You may have the Flu.",
    "possible_respiratory_infection": "You may have a Respiratory Infection.",
    "allergy": "You may be experiencing an Allergic Reaction.",
    "see_a_doctor": "Recommendation: Please consult a doctor.",
    "seek_urgent_care": "Recommendation: Seek urgent medical care.",
}

# All symptoms the system knows how to ask about
ALL_SYMPTOMS = [
    "cough", "sore_throat", "fever", "body_ache", "fatigue",
    "shortness_of_breath", "sneezing", "itchy_eyes", "runny_nose"
]


def get_user_symptoms():
    """
    Ask the user yes/no questions about each symptom.
    Returns a set of facts (symptoms the user confirmed having).
    """
    print("Answer with 'y' for yes or 'n' for no.\n")
    facts = set()
    for symptom in ALL_SYMPTOMS:
        readable = symptom.replace("_", " ")
        answer = input(f"Do you have {readable}? (y/n): ").strip().lower()
        if answer == "y":
            facts.add(symptom)
    return facts


def run_forward_chaining(facts):
    """
    Core inference engine.

    We loop through all rules repeatedly. Every time a rule's conditions
    are met by our current facts, we "fire" it: add its conclusion to our
    facts and record what happened in the log.

    We keep looping until a full pass over all rules produces no new facts.
    This is what allows CHAINING: a conclusion from one rule can satisfy
    the condition of another rule (e.g. common_cold -> see_a_doctor).
    """
    log = []            # human-readable trace of reasoning steps
    fired_rules = set()  # rule names we've already used, so we don't repeat them

    changed = True
    while changed:
        changed = False
        for rule in RULES:
            if rule["name"] in fired_rules:
                continue  # already applied this rule

            conditions_met = all(cond in facts for cond in rule["if"])

            if conditions_met:
                facts.add(rule["then"])
                fired_rules.add(rule["name"])
                log.append(
                    f"{rule['name']} fired: IF {rule['if']} -> THEN '{rule['then']}'"
                )
                changed = True  # a new fact was added, so loop again

    return facts, log


def main():
    print("=" * 50)
    print(" SIMPLE RULE-BASED EXPERT SYSTEM: SYMPTOM CHECKER")
    print("=" * 50)

    # Step 1: Collect facts from the user
    facts = get_user_symptoms()
    print("\nYour reported symptoms:", facts if facts else "None")

    # Step 2: Run the inference engine (forward chaining)
    final_facts, reasoning_log = run_forward_chaining(facts)

    # Step 3: Show the reasoning path (this is the "explainability" part)
    print("\n--- Reasoning Steps ---")
    if reasoning_log:
        for step in reasoning_log:
            print(step)
    else:
        print("No rules matched your symptoms.")

    # Step 4: Show final conclusions in plain English
    print("\n--- Conclusions ---")
    conclusions = [f for f in final_facts if f in CONCLUSION_MESSAGES]
    if conclusions:
        for c in conclusions:
            print("-", CONCLUSION_MESSAGES[c])
    else:
        print("No conclusion could be reached from the given symptoms.")

    print("\nNote: This is a simple educational demo, not real medical advice.")


if __name__ == "__main__":
    main()
