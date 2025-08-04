# Domain-driven feature engineering to capture known lexical representations of outcomes and modalities
# These are supplementary to the MeSH ontology pre-labeled in the PubMed records.
# Named-entity recognition is not used for primary outcomes and modalities,
#   however it is used later on in the ETL to extract biomarkers, drugs, and diseases. 
# The reason for excluding NER for exercise modality and outcome is due to increased risk of excess noise
#   relative to hand-crafted controlled vocabularies of de-facto standardized clinical/exercise terms.
outcome_keywords = [
    # Cardiometabolic
    "blood pressure", "systolic blood pressure", "diastolic blood pressure",
    "resting heart rate", "heart rate variability", "heart rate recovery",
    "cardiac function", "cardiac output", "stroke volume",
    "total cholesterol", "LDL", "HDL", "triglycerides",
    "glucose", "fasting glucose", "insulin sensitivity", "insulin resistance",
    # Body Composition
    "BMI", "body mass index", "waist circumference", "body fat percentage",
    "lean mass", "fat-free mass", "fat mass", "adiposity",
    "skeletal muscle mass", "muscle csa", "hypertrophy", "muscle hypertrophy",
    "muscle atrophy", "resting metabolic rate", "basal metabolic rate",
    # Muscular Strength/Power
    "muscle strength", "maximal strength", "grip strength",
    "isometric strength", "explosive strength", "muscle power", "power output", "peak torque",
    # Endurance/Aerobic Performance
    "VO2 max", "aerobic capacity", "oxygen consumption",
    "cardiorespiratory fitness", "endurance performance", "time to exhaustion",
    "lactate threshold", "anaerobic threshold", "fat oxidation rate",
    "peak aerobic power", "cycling time trial", "treadmill test", "distance run",
    "step test", "symptom-limited maximal cycle exercise test", "6 minute walk test",
    "6-minute walk distance", "incremental shuttle walk test", "exercise capacity",
    "relative exercise dose intensity",
    # Neuromotor / Coordination / Mobility
    "reaction time", "speed", "agility", "change of direction",
    "balance", "postural stability", "range of motion", "flexibility", "mobility",
    "motor coordination", "motor impairment", "gait", "gait speed", "walking speed",
    "functional capacity", "functional ambulation category", "fall risk",
    "sit-to-stand test", "timed up and go test", "short physical performance battery",
    # Bone / Joint / Musculoskeletal
    "bone density", "joint density", "muscle damage", "inflammation", "doms", "soreness", "recovery",
    # Cognitive / Psychological
    "cognitive function", "cognition", "cognitive score", "executive function",
    "behavior rating inventory of executive function",
    "mental health", "mood", "wellbeing", "stress", "depression", "anxiety",
    "sleep quality", "motivation", "self-efficacy", "perceived exertion",
    "exercise adherence", "fatigue perception", "fatigue",
    # Appetite / Hormonal
    "appetite", "satiety", "inflammatory markers", 
    # Energy Expenditure / Metabolic
    "resting metabolic rate", "basal metabolic rate",
    # Questionnaire-based outcomes
    "international physical activity questionnaire", "fugl-meyer upper extremity"]

mesh_mapping = {
    "Exercise": {
        "synonyms": ["physical activity", "training", "exercise training"],
        "modalities": [
            "combined exercise training",
            "functional training",
            "sports-specific training",
            "crossfit"
        ],
        "subterms": {
            "Aerobic Exercise": {
                "synonyms": ["cardio", "aerobic training"],
                "modalities": [
                    "aerobic exercise",
                    "endurance training",
                    "zone 1 cardio",
                    "zone 2 cardio",
                    "threshold training",
                    "moderate-intensity exercise",
                    "moderate-intensity training",
                    "moderate-intensity continuous exercise",
                    "moderate-to-vigorous intensity continuous training",
                    "low-intensity exercise",
                    "low-intensity training",
                    "low-intensity continuous endurance training",
                    "vigorous intensity",
                    "moderate-to-vigorous physical activity",
                    "light physical activity",
                    "speed endurance production",
                    "running",
                    "cycling",
                    "upright cycling",
                    "treadmill",
                    "rowing",
                    "swimming",
                    "ergometer",
                    "dance",
                    "zumba",
                    "kickboxing"
                ],
                "subterms": {}
            },
            "Resistance Training": {
                "synonyms": [
                    "strength training", "weight training", "weightlifting",
                    "resistance exercise", "acute resistance exercise",
                    "conventional resistance training", "eccentric resistance training",
                    "eccentric exercise"
                ],
                "modalities": [
                    "resistance exercise",
                    "acute resistance exercise",
                    "conventional resistance training",
                    "eccentric resistance training",
                    "eccentric exercise",
                    "strength training",
                    "bodyweight training",
                    "bodyweight exercise",
                    "isometric training",
                    "isometric exercise",
                    "elastic resistance training",
                    "freeweight training",
                    "freeweight exercise",
                    "olympic training",
                    "olympic weightlifting",
                    "olympic lifting",
                    "olympic weight training",
                    "weightlifting",
                    "bodybuilding",
                    "bodybuilding exercise",
                    "bodybuilding training"
                ],
                "subterms": {}
            },
            "High-Intensity Interval Training": {
                "synonyms": [
                    "hiit", "interval training", "high intensity exercise",
                    "high-intensity interval exercise"
                ],
                "modalities": [
                    "high-intensity interval training",
                    "high-intensity interval exercise",
                    "hiit",
                    "high intensity exercise"
                ],
                "subterms": {}
            },
            "Circuit-Based Exercise": {
                "synonyms": ["circuit training"],
                "modalities": [
                    "circuit training",
                    "circuit-based exercise",
                    "crossfit"
                ],
                "subterms": {}
            },
            "Plyometric Exercise": {
                "synonyms": ["jump training", "explosive training"],
                "modalities": [
                    "plyometric exercise"
                ],
                "subterms": {}
            },
            "Periodization": {
                "synonyms": ["training periodization", "training cycles"],
                "modalities": [
                    "periodization"
                ],
                "subterms": {}
            },
            "Muscle Stretching Exercises": {
                "synonyms": [
                    "stretching", "flexibility training", "flexibility exercise"
                ],
                "modalities": [
                    "flexibility training",
                    "flexibility exercise"
                ],
                "subterms": {}
            },
            "Flexibility and Stability / Mind-Body": {
                "synonyms": [
                    "balance training", "balance exercise",
                    "stability training", "stability exercise",
                    "yoga", "pilates", "pilates reformer",
                    "tai chi", "mind-body exercise"
                ],
                "modalities": [
                    "balance training",
                    "balance exercise",
                    "stability training",
                    "stability exercise",
                    "yoga",
                    "pilates",
                    "pilates reformer",
                    "tai chi",
                    "mind-body exercise"
                ],
                "subterms": {}
            }
        }
    },
    "Physical Conditioning, Human": {
        "synonyms": ["physical fitness", "conditioning"],
        "modalities": [
            "moderate-intensity continuous exercise",
            "low-intensity training",
            "moderate-to-vigorous intensity continuous training"
        ],
        "subterms": {}
    },
    "Resistance Training": {
        "synonyms": [
            "strength training", "weight training", "weightlifting",
            "resistance exercise"
        ],
        "modalities": [
            "resistance exercise",
            "acute resistance exercise",
            "conventional resistance training",
            "eccentric resistance training",
            "eccentric exercise",
            "strength training",
            "bodyweight training",
            "bodyweight exercise",
            "isometric training",
            "isometric exercise",
            "elastic resistance training",
            "freeweight training",
            "freeweight exercise",
            "olympic training",
            "olympic weightlifting",
            "olympic lifting",
            "olympic weight training",
            "weightlifting",
            "bodybuilding",
            "bodybuilding exercise",
            "bodybuilding training"
        ],
        "subterms": {}
    },
    "Aerobic Exercise": {
        "synonyms": ["cardio", "endurance exercise"],
        "modalities": [
            "aerobic exercise",
            "endurance training",
            "zone 1 cardio",
            "zone 2 cardio",
            "threshold training",
            "moderate-intensity exercise",
            "moderate-intensity training",
            "moderate-intensity continuous exercise",
            "moderate-to-vigorous intensity continuous training",
            "low-intensity exercise",
            "low-intensity training",
            "low-intensity continuous endurance training",
            "vigorous intensity",
            "moderate-to-vigorous physical activity",
            "light physical activity",
            "speed endurance production",
            "running",
            "cycling",
            "upright cycling",
            "treadmill",
            "rowing",
            "swimming",
            "ergometer",
            "dance",
            "zumba",
            "kickboxing"
        ],
        "subterms": {}
    },
    "Circuit-Based Exercise": {
        "synonyms": ["circuit training"],
        "modalities": [
            "circuit training",
            "circuit-based exercise",
            "crossfit"
        ],
        "subterms": {}
    },
    "Periodization": {
        "synonyms": ["training cycles", "training periodization"],
        "modalities": [
            "periodization"
        ],
        "subterms": {}
    },
    "Weight Lifting": {
        "synonyms": ["weightlifting", "weight training", "freeweight training"],
        "modalities": [
            "weightlifting",
            "freeweight training",
            "freeweight exercise",
            "olympic training",
            "olympic weightlifting",
            "olympic lifting",
            "olympic weight training"
        ],
        "subterms": {}
    },
    "High-Intensity Interval Training": {
        "synonyms": [
            "hiit", "interval training", "high intensity exercise",
            "high-intensity interval exercise"
        ],
        "modalities": [
            "high-intensity interval training",
            "high-intensity interval exercise",
            "hiit",
            "high intensity exercise"
        ],
        "subterms": {}
    },
    "Plyometric Exercise": {
        "synonyms": ["jump training", "explosive training"],
        "modalities": [
            "plyometric exercise"
        ],
        "subterms": {}
    },
    "Endurance Training": {
        "synonyms": ["aerobic exercise", "cardio", "long-duration exercise"],
        "modalities": [
            "endurance training",
            "aerobic exercise",
            "zone 1 cardio",
            "zone 2 cardio",
            "threshold training",
            "moderate-intensity exercise",
            "moderate-intensity training",
            "moderate-intensity continuous exercise",
            "moderate-to-vigorous intensity continuous training",
            "low-intensity exercise",
            "low-intensity training",
            "low-intensity continuous endurance training",
            "vigorous intensity",
            "moderate-to-vigorous physical activity",
            "light physical activity",
            "speed endurance production"
        ],
        "subterms": {}
    },
    "Muscle Stretching Exercises": {
        "synonyms": ["stretching", "flexibility exercises"],
        "modalities": [
            "flexibility training",
            "flexibility exercise"
        ],
        "subterms": {}
    },
    "Physical Fitness": {
        "synonyms": ["fitness", "physical conditioning", "physical health"],
        "modalities": [
            "moderate-intensity continuous exercise",
            "low-intensity training",
            "moderate-to-vigorous intensity continuous training",
            "light physical activity"
        ],
        "subterms": {}
    },
    "Cardiorespiratory Fitness": {
        "synonyms": ["aerobic fitness", "cardio fitness"],
        "modalities": [
            "endurance training",
            "aerobic exercise",
            "running",
            "cycling",
            "swimming",
            "rowing",
            "treadmill"
        ],
        "subterms": {}
    },
    "Exercise Therapy": {
        "synonyms": ["rehabilitation exercise", "rehab", "therapeutic exercise"],
        "modalities": [
            "rehabilitation exercise",
            "cardiac rehab",
            "pulmonary rehab",
            "post-stroke exercise",
            "occupational therapy exercise"
        ],
        "subterms": {}
    },
    "Walking": {
        "synonyms": ["gait training", "walking exercise", "walking therapy"],
        "modalities": [
            "walking",
            "gait",
            "gait speed",
            "walking speed"
        ],
        "subterms": {}
    },
    "Swimming": {
        "synonyms": [],
        "modalities": [
            "swimming"
        ],
        "subterms": {}
    },
    "Gymnastics": {
        "synonyms": [],
        "modalities": [
            "gymnastics"
        ],
        "subterms": {}
    },
    "Bicycling": {
        "synonyms": ["cycling", "upright cycling"],
        "modalities": [
            "cycling",
            "upright cycling"
        ],
        "subterms": {}
    }
}