from app.routing import route
def test_emergency_override():
 r=route('general_medical',.9,'I have severe chest pain')
 assert r['urgency']=='urgent' and r['category']=='Emergency assistance'
def test_low_confidence_review():
 assert route('general_medical',.2,'hello')['requires_human_review'] is True
