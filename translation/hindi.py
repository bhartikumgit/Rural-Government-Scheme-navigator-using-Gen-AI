"""
hindi.py — Hindi translation for Rural Scheme Navigator
========================================================
Strategy: Pre-translated static strings for UI elements +
lightweight neural translation for plain summary sentences only.

Why not full neural translation:
  Government text has too many acronyms (MGNREGS, PM-KISAN),
  proper nouns, and technical terms for opus-mt or NLLB to
  handle reliably without domain fine-tuning.

  This is exactly what myscheme.gov.in does — their Hindi
  version uses pre-translated static content.

For plain summary sentences (no acronyms, simple English)
we use a simple word-level translation dictionary approach
that is fast, deterministic, and correct.
"""

# ── Pre-translated UI strings ──
UI_STRINGS = {
    "Why you are eligible":        "आप पात्र क्यों हैं",
    "What you get":                "आपको क्या मिलेगा",
    "Documents you need":          "आवश्यक दस्तावेज़",
    "How to apply — step by step": "आवेदन कैसे करें — चरण दर चरण",
    "Benefit / Assistance Amount": "लाभ / सहायता राशि",
    "Quick Tips":                  "महत्वपूर्ण सुझाव",
    "Useful Contacts":             "उपयोगी संपर्क",
    "scheme found for you":        "योजना आपके लिए मिली",
    "schemes found for you":       "योजनाएं आपके लिए मिलीं",
    "HIGH confidence":             "उच्च विश्वास",
    "MEDIUM confidence":           "मध्यम विश्वास",
    "LOW confidence":              "कम विश्वास",
    "New Search":                  "नई खोज",
    "Apply at Official Portal":    "आधिकारिक पोर्टल पर आवेदन करें",
}

# ── Pre-translated category summaries ──
# These replace the neural model for scheme summaries
CATEGORY_SUMMARIES_HI = {
    "Agriculture": (
        "यह योजना किसानों को सीधे वित्तीय सहायता प्रदान करती है। "
        "आप पात्र हैं और सफलतापूर्वक आवेदन करने पर लाभ प्राप्त कर सकते हैं।"
    ),
    "Housing": (
        "यह योजना सरकारी सहायता से पक्का घर बनाने में मदद करती है। "
        "आप पात्र हैं और आवेदन करने पर निर्माण सहायता मिलेगी।"
    ),
    "Employment": (
        "यह योजना ग्रामीण परिवारों को रोजगार और मजदूरी की गारंटी देती है। "
        "आप पात्र हैं और आवेदन करने पर लाभ प्राप्त कर सकते हैं।"
    ),
    "Financial Inclusion": (
        "यह योजना आपको बैंकिंग सेवाओं और बीमा तक पहुंच देती है। "
        "आप पात्र हैं — नजदीकी बैंक शाखा में जाएं।"
    ),
    "Health": (
        "यह योजना आपके परिवार को अस्पताल में मुफ्त या कैशलेस इलाज देती है। "
        "आप पात्र हैं और किसी भी सूचीबद्ध अस्पताल में इलाज करा सकते हैं।"
    ),
    "Education": (
        "यह योजना आपकी शिक्षा के लिए वित्तीय सहायता प्रदान करती है। "
        "आप पात्र हैं — छात्रवृत्ति पोर्टल पर आवेदन करें।"
    ),
    "Financial Assistance": (
        "यह योजना आपकी आजीविका शुरू करने के लिए ऋण या अनुदान प्रदान करती है। "
        "आप पात्र हैं और बैंक के माध्यम से आवेदन कर सकते हैं।"
    ),
    "Social Security": (
        "यह योजना बहुत कम प्रीमियम पर आपके परिवार की सुरक्षा करती है। "
        "आप पात्र हैं — अपने बैंक में जाकर नामांकन करें।"
    ),
    "Social Welfare": (
        "यह योजना आपके दैनिक जीवन को बेहतर बनाने के लिए सरकारी सहायता देती है। "
        "आप पात्र हैं और नजदीकी सरकारी कार्यालय में आवेदन कर सकते हैं।"
    ),
    "Skill Development": (
        "यह योजना आपको मुफ्त कौशल प्रशिक्षण और बेहतर रोजगार दिलाने में मदद करती है। "
        "आप पात्र हैं — नजदीकी प्रशिक्षण केंद्र में नामांकन करें।"
    ),
    "Women and Child Development": (
        "यह योजना महिलाओं और बच्चों को वित्तीय सहायता और सुरक्षा प्रदान करती है। "
        "आप पात्र हैं — आंगनवाड़ी या ब्लॉक कार्यालय में आवेदन करें।"
    ),
    "Infrastructure": (
        "यह योजना आपके गांव में सड़क और बुनियादी सुविधाएं प्रदान करती है। "
        "ग्राम पंचायत के माध्यम से आवेदन करें।"
    ),
}

# ── Pre-translated eligibility reasons ──
ELIGIBILITY_PHRASES_HI = {
    "You qualify because":
        "आप पात्र हैं क्योंकि",
    "Age": "आयु",
    "is within required range":
        "आवश्यक सीमा के भीतर है",
    "Caste category": "जाति वर्ग",
    "is eligible": "पात्र है",
    "Occupation": "व्यवसाय",
    "matches scheme requirement":
        "योजना की आवश्यकता से मेल खाता है",
    "Central government scheme — open to all states":
        "केंद्र सरकार की योजना — सभी राज्यों के लिए खुली है",
    "Rural residence requirement met":
        "ग्रामीण निवास की आवश्यकता पूरी होती है",
    "Urban residence requirement met":
        "शहरी निवास की आवश्यकता पूरी होती है",
    "Income": "आय",
    "is within limit": "सीमा के भीतर है",
    "Gender requirement": "लिंग आवश्यकता",
    "met": "पूरी होती है",
    "You are a resident of": "आप निवासी हैं",
    "eligible for state scheme":
        "राज्य योजना के लिए पात्र हैं",
    "Land ownership suggests farming activity":
        "भूमि स्वामित्व कृषि गतिविधि का संकेत देता है",
    "likely eligible": "संभवतः पात्र हैं",
}

# ── Pre-translated document names ──
DOCUMENTS_HI = {
    "Aadhaar card":                     "आधार कार्ड",
    "Bank account passbook":            "बैंक खाता पासबुक",
    "Land records":                     "भूमि अभिलेख",
    "Land records / Khasra-Khatauni":   "भूमि अभिलेख / खसरा-खतौनी",
    "BPL certificate":                  "BPL प्रमाण पत्र",
    "BPL certificate or SECC 2011 inclusion": "BPL प्रमाण पत्र या SECC 2011 समावेश",
    "Caste certificate (if SC/ST/OBC)": "जाति प्रमाण पत्र (SC/ST/OBC के लिए)",
    "SC caste certificate":             "SC जाति प्रमाण पत्र",
    "ST caste certificate":             "ST जाति प्रमाण पत्र",
    "OBC non-creamy layer certificate": "OBC नॉन-क्रीमी लेयर प्रमाण पत्र",
    "Income certificate":               "आय प्रमाण पत्र",
    "Residence proof":                  "निवास प्रमाण",
    "Address proof":                    "पता प्रमाण",
    "Domicile certificate":             "अधिवास प्रमाण पत्र",
    "Mobile number linked to Aadhaar":  "आधार से जुड़ा मोबाइल नंबर",
    "Mobile number":                    "मोबाइल नंबर",
    "Passport-size photograph":         "पासपोर्ट आकार की फोटो",
    "Photograph":                       "फोटो",
    "PAN card":                         "PAN कार्ड",
    "Voter ID":                         "मतदाता पहचान पत्र",
    "Birth certificate":                "जन्म प्रमाण पत्र",
    "Age proof":                        "आयु प्रमाण",
    "Project report":                   "परियोजना रिपोर्ट",
    "Mark sheet of previous exam":      "पिछली परीक्षा की मार्कशीट",
    "Class 12 mark sheet and certificate": "कक्षा 12 की मार्कशीट और प्रमाण पत्र",
    "Enrollment certificate from institution": "संस्थान से नामांकन प्रमाण पत्र",
    "MCH card / ANC registration at ASHA": "MCH कार्ड / ASHA में ANC पंजीकरण",
    "Disability certificate":           "विकलांगता प्रमाण पत्र",
    "Death certificate of husband":     "पति का मृत्यु प्रमाण पत्र",
    "Marriage invitation card or certificate": "विवाह आमंत्रण पत्र या प्रमाण पत्र",
    "ECHS smart card":                  "ECHS स्मार्ट कार्ड",
    "Discharge book":                   "डिस्चार्ज बुक",
    "Ration card":                      "राशन कार्ड",
}

# ── Pre-translated common apply step phrases ──
# ── Expanded document translation table ──
DOCUMENTS_HI = {
    "Aadhaar card": "आधार कार्ड",
    "Bank account passbook": "बैंक खाता पासबुक",
    "Bank account with auto-debit facility": "ऑटो-डेबिट सुविधा वाला बैंक खाता",
    "Bank account with auto-debit": "ऑटो-डेबिट वाला बैंक खाता",
    "Bank account details": "बैंक खाता विवरण",
    "Bank account in girl's name": "बालिका के नाम पर बैंक खाता",
    "Bank account passbook (in applicant's name)": "आवेदक के नाम पर बैंक खाता पासबुक",
    "Land records": "भूमि अभिलेख",
    "Land records / Khasra-Khatauni": "भूमि अभिलेख / खसरा-खतौनी",
    "Land ownership documents": "भूमि स्वामित्व दस्तावेज़",
    "Land ownership documents / Khasra": "भूमि स्वामित्व दस्तावेज़ / खसरा",
    "Land ownership documents or consent from Gram Panchayat": "भूमि दस्तावेज़ या ग्राम पंचायत की सहमति",
    "BPL certificate": "BPL प्रमाण पत्र",
    "BPL certificate or SECC 2011 inclusion": "BPL प्रमाण पत्र या SECC 2011 समावेश",
    "BPL ration card OR SECC 2011 inclusion": "BPL राशन कार्ड या SECC 2011 समावेश",
    "BPL or ration card": "BPL या राशन कार्ड",
    "Caste certificate (if SC/ST/OBC)": "जाति प्रमाण पत्र (SC/ST/OBC के लिए)",
    "SC caste certificate": "SC जाति प्रमाण पत्र",
    "SC caste certificate from Bihar authority": "बिहार प्राधिकरण से SC जाति प्रमाण पत्र",
    "SC/ST caste certificate": "SC/ST जाति प्रमाण पत्र",
    "ST caste certificate": "ST जाति प्रमाण पत्र",
    "ST caste certificate from competent authority": "सक्षम प्राधिकारी से ST जाति प्रमाण पत्र",
    "OBC non-creamy layer certificate": "OBC नॉन-क्रीमी लेयर प्रमाण पत्र",
    "Caste certificate for SC/ST/OBC": "SC/ST/OBC के लिए जाति प्रमाण पत्र",
    "Income certificate": "आय प्रमाण पत्र",
    "Income certificate (family income below Rs. 2.5 lakh)": "आय प्रमाण पत्र (पारिवारिक आय 2.5 लाख से कम)",
    "Income certificate (annual family income up to 3 lakh)": "आय प्रमाण पत्र (वार्षिक पारिवारिक आय 3 लाख तक)",
    "Income declaration": "आय घोषणा",
    "Residence proof": "निवास प्रमाण",
    "Address proof": "पता प्रमाण",
    "Domicile certificate": "अधिवास प्रमाण पत्र",
    "Bihar domicile certificate": "बिहार अधिवास प्रमाण पत्र",
    "Bihar domicile/residence certificate": "बिहार अधिवास/निवास प्रमाण पत्र",
    "UP domicile/residence proof": "UP अधिवास/निवास प्रमाण",
    "Rajasthan domicile certificate": "राजस्थान अधिवास प्रमाण पत्र",
    "Madhya Pradesh domicile certificate": "मध्य प्रदेश अधिवास प्रमाण पत्र",
    "Jharkhand domicile certificate": "झारखंड अधिवास प्रमाण पत्र",
    "Assam domicile certificate": "असम अधिवास प्रमाण पत्र",
    "West Bengal domicile certificate": "पश्चिम बंगाल अधिवास प्रमाण पत्र",
    "Odisha domicile": "ओडिशा अधिवास",
    "Karnataka domicile certificate": "कर्नाटक अधिवास प्रमाण पत्र",
    "Mobile number linked to Aadhaar": "आधार से जुड़ा मोबाइल नंबर",
    "Mobile number": "मोबाइल नंबर",
    "Passport-size photograph": "पासपोर्ट आकार की फोटो",
    "Photograph": "फोटो",
    "Photograph of girl and parent": "बालिका और माता-पिता की फोटो",
    "PAN card": "PAN कार्ड",
    "PAN card or Form 60": "PAN कार्ड या फॉर्म 60",
    "Voter ID": "मतदाता पहचान पत्र",
    "Voter ID / PAN card / Passport / NREGA Job Card / Driving Licence": "मतदाता ID / PAN / पासपोर्ट / NREGA जॉब कार्ड / ड्राइविंग लाइसेंस",
    "Birth certificate": "जन्म प्रमाण पत्र",
    "Birth certificate of girl child": "बालिका का जन्म प्रमाण पत्र",
    "Age proof": "आयु प्रमाण",
    "Age proof (birth certificate or school certificate or Aadhaar)": "आयु प्रमाण (जन्म प्रमाण पत्र या स्कूल प्रमाण पत्र या आधार)",
    "Age proof of girl (18 years or above) — school certificate or birth certificate": "बालिका का आयु प्रमाण (18 वर्ष या अधिक)",
    "Project report": "परियोजना रिपोर्ट",
    "Project report for the proposed enterprise": "प्रस्तावित उद्यम की परियोजना रिपोर्ट",
    "Project report for proposed enterprise": "प्रस्तावित उद्यम की परियोजना रिपोर्ट",
    "Mark sheet of previous exam": "पिछली परीक्षा की मार्कशीट",
    "Mark sheet of qualifying exam with minimum 60% marks": "न्यूनतम 60% अंकों के साथ योग्यता परीक्षा की मार्कशीट",
    "Previous year mark sheet": "पिछले वर्ष की मार्कशीट",
    "Class 12 mark sheet and certificate": "कक्षा 12 की मार्कशीट और प्रमाण पत्र",
    "Class 8 pass certificate": "कक्षा 8 उत्तीर्ण प्रमाण पत्र",
    "Class 8 pass or ITI or diploma": "कक्षा 8 उत्तीर्ण या ITI या डिप्लोमा",
    "Educational certificate": "शैक्षिक प्रमाण पत्र",
    "Educational qualification certificate": "शैक्षणिक योग्यता प्रमाण पत्र",
    "Educational certificates": "शैक्षिक प्रमाण पत्र",
    "Matric (Class 10) pass certificate": "मैट्रिक (कक्षा 10) उत्तीर्ण प्रमाण पत्र",
    "Enrollment certificate from institution": "संस्थान से नामांकन प्रमाण पत्र",
    "Institution enrollment certificate": "संस्थान नामांकन प्रमाण पत्र",
    "Bonafide student certificate": "बोनाफाइड छात्र प्रमाण पत्र",
    "School enrollment certificate": "स्कूल नामांकन प्रमाण पत्र",
    "Admission letter from college": "कॉलेज से प्रवेश पत्र",
    "College enrollment certificate": "कॉलेज नामांकन प्रमाण पत्र",
    "MCH card / ANC registration at ASHA": "MCH कार्ड / ASHA में ANC पंजीकरण",
    "MCH card or ANC registration": "MCH कार्ड या ANC पंजीकरण",
    "Disability certificate": "विकलांगता प्रमाण पत्र",
    "Disability certificate (minimum 40% disability from competent authority)": "विकलांगता प्रमाण पत्र (न्यूनतम 40% विकलांगता)",
    "Death certificate of husband": "पति का मृत्यु प्रमाण पत्र",
    "Death certificate of breadwinner": "परिवार के मुखिया का मृत्यु प्रमाण पत्र",
    "Relationship proof with deceased": "मृतक से संबंध का प्रमाण",
    "Nominee details": "नामांकित व्यक्ति का विवरण",
    "Marriage invitation card or certificate": "विवाह आमंत्रण पत्र या प्रमाण पत्र",
    "Unmarried declaration": "अविवाहित घोषणा",
    "ECHS smart card": "ECHS स्मार्ट कार्ड",
    "Discharge book": "डिस्चार्ज बुक",
    "Discharge book of Ex-Serviceman parent": "पूर्व सैनिक माता-पिता की डिस्चार्ज बुक",
    "PPO (Pension Payment Order)": "PPO (पेंशन भुगतान आदेश)",
    "Service certificate from employer": "नियोक्ता से सेवा प्रमाण पत्र",
    "Ration card": "राशन कार्ड",
    "Ration card (if included via SECC/RSBY)": "राशन कार्ड (SECC/RSBY के माध्यम से)",
    "Jan Aadhaar card (Rajasthan)": "जन आधार कार्ड (राजस्थान)",
    "ESIC card (issued by employer)": "ESIC कार्ड (नियोक्ता द्वारा जारी)",
    "Employer registration certificate": "नियोक्ता पंजीकरण प्रमाण पत्र",
    "EPFO registration of employer": "नियोक्ता का EPFO पंजीकरण",
    "UAN (Universal Account Number)": "UAN (सार्वभौमिक खाता संख्या)",
    "Udyam Registration Certificate": "उद्यम पंजीकरण प्रमाण पत्र",
    "Business plan / project report": "व्यवसाय योजना / परियोजना रिपोर्ट",
    "Proof of business address": "व्यवसाय पते का प्रमाण",
    "Business registration certificate": "व्यवसाय पंजीकरण प्रमाण पत्र",
    "Incorporation certificate (company or LLP)": "निगमन प्रमाण पत्र (कंपनी या LLP)",
    "No existing house proof": "कोई मौजूदा मकान नहीं का प्रमाण",
    "Property documents or allotment letter": "संपत्ति दस्तावेज़ या आवंटन पत्र",
    "Sowing certificate from Patwari": "पटवारी से बुवाई प्रमाण पत्र",
    "Crop loan passbook (if loanee farmer)": "फसल ऋण पासबुक (यदि ऋणी किसान हैं)",
    "Quotation from empanelled vendor": "सूचीबद्ध विक्रेता से कोटेशन",
    "Existing pump details": "मौजूदा पंप का विवरण",
    "LPG consumer number": "LPG उपभोक्ता संख्या",
    "Certificate of vending from Urban Local Body": "शहरी स्थानीय निकाय से वेंडिंग प्रमाण पत्र",
    "Doctor's prescription": "डॉक्टर का पर्चा",
    "Medical diagnosis certificate": "चिकित्सा निदान प्रमाण पत्र",
    "TB diagnosis certificate from government DOTS centre": "सरकारी DOTS केंद्र से TB निदान प्रमाण पत्र",
    "Apprenticeship agreement signed with employer": "नियोक्ता के साथ हस्ताक्षरित प्रशिक्षुता समझौता",
    "SHG membership certificate": "SHG सदस्यता प्रमाण पत्र",
    "Self-declaration of unorganised worker status": "असंगठित श्रमिक स्थिति की स्व-घोषणा",
    "Competitive exam qualification proof": "प्रतियोगी परीक्षा योग्यता प्रमाण",
    "Unemployment certificate": "बेरोजगारी प्रमाण पत्र",
    "Pattadar passbook (land records)": "पट्टेदार पासबुक (भूमि अभिलेख)",
    "Two guarantors or collateral": "दो गारंटर या संपार्श्विक",
    "No existing loan default certificate": "कोई मौजूदा ऋण चूक नहीं का प्रमाण पत्र",
    "Any ID for non-emergency services": "गैर-आपातकालीन सेवाओं के लिए कोई भी ID",
    "No documents required for emergency assistance": "आपातकालीन सहायता के लिए कोई दस्तावेज़ आवश्यक नहीं",
    "Group formation certificate if cluster": "क्लस्टर होने पर समूह गठन प्रमाण पत्र",
    "Initial deposit (minimum Rs. 250)": "प्रारंभिक जमा (न्यूनतम Rs. 250)",
    "Aadhaar of parent/guardian": "माता-पिता/अभिभावक का आधार",
    "Address proof of parent": "माता-पिता का पता प्रमाण",
    "SHG meeting records": "SHG बैठक के रिकॉर्ड",
    "Bank account of SHG": "SHG का बैंक खाता",
    "Land/water body documents": "भूमि/जल निकाय दस्तावेज़",
    "Land document (for agriculture-linked loans)": "भूमि दस्तावेज़ (कृषि-संबंधित ऋण के लिए)",
    "Land records if available": "यदि उपलब्ध हो तो भूमि अभिलेख",
    "Land/plot documents or allotment letter": "भूमि/प्लॉट दस्तावेज़ या आवंटन पत्र",
    "Dependent family member documents": "आश्रित परिवार के सदस्य के दस्तावेज़",
    "Proof of trade (self declaration accepted)": "व्यापार का प्रमाण (स्व-घोषणा स्वीकार्य)",
    "ITR if available": "यदि उपलब्ध हो तो ITR",
    "Bank account statement (last 6 months if existing business)": "बैंक खाता विवरण (मौजूदा व्यवसाय के लिए पिछले 6 माह)",
    "Child's birth certificate": "बच्चे का जन्म प्रमाण पत्र",
    "Proof of child's orphan or destitute status": "बच्चे की अनाथ या निराश्रित स्थिति का प्रमाण",
}

# ── Expanded step phrases ──
STEP_PHRASES_HI = {
    "Visit nearest Common Service Centre": "नजदीकी Common Service Centre (CSC) जाएं",
    "Visit nearest": "नजदीकी जाएं",
    "Visit any": "किसी भी जाएं",
    "Common Service Centre": "Common Service Centre (CSC)",
    "Gram Panchayat": "ग्राम पंचायत",
    "Block Development Office": "खंड विकास कार्यालय",
    "Block Development Officer": "खंड विकास अधिकारी",
    "nearest bank branch": "नजदीकी बैंक शाखा",
    "bank branch": "बैंक शाखा",
    "Submit": "जमा करें",
    "Submit with": "के साथ जमा करें",
    "Fill": "भरें",
    "Fill the": "भरें",
    "Apply online at": "पर ऑनलाइन आवेदन करें",
    "Apply at": "पर आवेदन करें",
    "Download": "डाउनलोड करें",
    "Register": "पंजीकरण करें",
    "Register at": "पर पंजीकरण करें",
    "Amount credited to bank account": "राशि बैंक खाते में जमा की जाएगी",
    "credited to bank account": "बैंक खाते में जमा किया जाएगा",
    "free of cost": "बिल्कुल मुफ्त",
    "within 15 days": "15 दिनों के भीतर",
    "within 30 days": "30 दिनों के भीतर",
    "within 7 days": "7 दिनों के भीतर",
    "within 10 days": "10 दिनों के भीतर",
    "Aadhaar card": "आधार कार्ड",
    "bank account": "बैंक खाता",
    "application form": "आवेदन पत्र",
    "documents": "दस्तावेज़",
    "verification": "सत्यापन",
    "approved": "स्वीकृत",
    "sanctioned": "स्वीकृत",
    "disbursed": "वितरित",
    "issued": "जारी किया गया",
    "automatically": "स्वचालित रूप से",
    "installments": "किश्तों में",
    "monthly": "प्रति माह",
    "annually": "वार्षिक",
    "No separate application needed": "कोई अलग आवेदन आवश्यक नहीं",
    "No separate application required": "कोई अलग आवेदन आवश्यक नहीं",
    "Pension credited": "पेंशन जमा की जाएगी",
    "Scholarship credited": "छात्रवृत्ति जमा की जाएगी",
    "Check eligibility at": "पर पात्रता जांचें",
    "Attend": "भाग लें",
    "Receive": "प्राप्त करें",
    "Contact nearest": "नजदीकी से संपर्क करें",
    "Confirm when done": "पूरा होने पर पुष्टि करें",
    "construction": "निर्माण",
    "installation": "स्थापना",
    "training": "प्रशिक्षण",
    "empanelled hospital": "सूचीबद्ध अस्पताल",
    "government hospital": "सरकारी अस्पताल",
}


def translate_document(doc: str) -> str:
    """Translate a document name to Hindi using lookup table."""
    return DOCUMENTS_HI.get(doc, doc)


def translate_summary_for_category(category: str, profile_info: str = "") -> str:
    """Get pre-translated summary for a scheme category."""
    return CATEGORY_SUMMARIES_HI.get(
        category,
        "यह योजना आपके लिए उपलब्ध है। आवेदन करने के लिए नजदीकी कार्यालय जाएं।"
    )


def translate_eligibility(explanation: str) -> str:
    """Translate eligibility explanation using phrase replacement."""
    result = explanation
    for en, hi in ELIGIBILITY_PHRASES_HI.items():
        result = result.replace(en, hi)
    return result


def translate_step(step: str) -> str:
    """Translate an application step using phrase replacement."""
    result = step
    for en, hi in STEP_PHRASES_HI.items():
        result = result.replace(en, hi)
    return result


def translate_document(doc: str) -> str:
    """Translate a document name to Hindi using lookup table."""
    return DOCUMENTS_HI.get(doc, doc)


def translate_summary_for_category(category: str, profile_info: str = "") -> str:
    """Get pre-translated summary for a scheme category."""
    return CATEGORY_SUMMARIES_HI.get(
        category,
        "यह योजना आपके लिए उपलब्ध है। आवेदन करने के लिए नजदीकी कार्यालय जाएं।"
    )


def translate_eligibility(explanation: str) -> str:
    """
    Translate eligibility explanation using phrase replacement.
    Works on the structured output from our rule-based engine.
    """
    result = explanation
    for en, hi in ELIGIBILITY_PHRASES_HI.items():
        result = result.replace(en, hi)
    return result


def translate_step(step: str) -> str:
    """
    Translate an application step using phrase replacement.
    Keeps scheme names, URLs, and portal names in English.
    """
    result = step
    for en, hi in STEP_PHRASES_HI.items():
        result = result.replace(en, hi)
    return result


class HindiTranslator:
    """
    Hindi translation using pre-translated static strings.
    Fast, deterministic, zero model errors.
    """

    def __init__(self):
        # No model to load — instant initialization
        pass

    def translate(self, text: str) -> str:
        """
        Translate plain English text to Hindi.
        Uses phrase lookup — no neural model.
        """
        if not text:
            return text
        result = text
        for en, hi in ELIGIBILITY_PHRASES_HI.items():
            result = result.replace(en, hi)
        for en, hi in STEP_PHRASES_HI.items():
            result = result.replace(en, hi)
        return result

    def translate_batch(self, texts: list) -> list:
        return [self.translate(t) for t in texts]

    def translate_scheme_response(self, scheme: dict) -> dict:
        """
        Translate all fields of a scheme response dict.
        Uses category-based summary + phrase lookup for other fields.
        """
        translated = dict(scheme)

        # Summary — use category-based pre-translated text
        category = scheme.get("category", "")
        translated["plain_summary_hi"] = translate_summary_for_category(category)

        # Eligibility explanation — phrase replacement
        explanation = scheme.get("eligibility_explanation", "")
        translated["eligibility_explanation_hi"] = translate_eligibility(explanation)

        # What you get — phrase replacement
        what = scheme.get("what_you_get", "")
        translated["what_you_get_hi"] = self.translate(what)

        # Documents — lookup table
        docs = scheme.get("documents_needed", [])
        translated["documents_needed_hi"] = [
            translate_document(d) for d in docs
        ]

        # Steps — phrase replacement
        steps = scheme.get("how_to_apply", [])
        translated["how_to_apply_hi"] = [
            translate_step(s) for s in steps
        ]

        # Warnings — phrase replacement
        warnings = scheme.get("warnings", [])
        translated["warnings_hi"] = [
            self.translate(w) for w in warnings
        ]

        return translated

    def translate_summary(self, summary: str) -> str:
        return self.translate(summary)


# ── Standalone test ──
if __name__ == "__main__":
    translator = HindiTranslator()

    print("\nTEST — Document translation:")
    docs = [
        "Aadhaar card",
        "BPL certificate",
        "Land records / Khasra-Khatauni",
        "Income certificate",
        "Passport-size photograph",
    ]
    for d in docs:
        print(f"  EN: {d}")
        print(f"  HI: {translate_document(d)}\n")

    print("\nTEST — Category summaries:")
    for cat in ["Agriculture", "Health", "Employment", "Education"]:
        print(f"\n  [{cat}]")
        print(f"  {translate_summary_for_category(cat)}")

    print("\nTEST — Eligibility translation:")
    explanations = [
        "You qualify because: Age 35 is within required range; Caste category SC is eligible.",
        "You qualify because: Occupation 'Farmer' matches scheme requirement; Central government scheme — open to all states.",
    ]
    for e in explanations:
        print(f"\n  EN: {e}")
        print(f"  HI: {translate_eligibility(e)}")