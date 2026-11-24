CATEGORIES={
'general_medical':('General medical consultation','General Physician','routine'),
'maternal_child':('Maternal & child healthcare','Maternal / Paediatric care','routine'),
'mental_health':('Mental health support','Mental health professional','routine'),
'preventive':('Preventive healthcare','Preventive care clinic','routine'),
'chronic':('Chronic disease support','Chronic care consultation','routine'),
'medication':('Medication information','Pharmacist / clinician information service','routine'),
'specialist':('Specialist consultation','Specialist consultation desk','routine'),
'emergency':('Emergency assistance','Emergency medical services','urgent'),
'other':('Other / unclassified','General healthcare navigation','review')}

EMERGENCY_TERMS=[
    'chest pain','difficulty breathing','cannot breathe','severe bleeding','unconscious',
    'fainted','stroke','face drooping','suicidal','overdose','seizure','severe allergic reaction'
]

def route(category,confidence,text):
    lower=text.lower()
    safety_override=any(term in lower for term in EMERGENCY_TERMS)
    if safety_override:
        category='emergency'; confidence=max(confidence,.95)
    label,destination,urgency=CATEGORIES.get(category,CATEGORIES['other'])
    return {
        'category':label,
        'confidence':float(confidence),
        'urgency':urgency,
        'requires_human_review':bool(confidence<0.60 or category=='other'),
        'destination':destination,
        'safety_override':safety_override,
    }
