def modify_tissue_data_key(x: str) -> str:
    modified_key = x.replace("Tissue RNA - ", "").replace(" [nTPM]", "").capitalize()
    if modified_key in ["Endometrium 1", "Skin 1", "Stomach 1"]:
        modified_key = modified_key.replace(" 1", "")

    return modified_key


TISSUE_PLOT_ATTRIBUTES = [
    # Brain
    {
        "organ": "Brain",
        "tissue": "Cerebral cortex",
        "order": 0,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Cerebellum",
        "order": 1,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Basal ganglia",
        "order": 2,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Hypothalamus",
        "order": 3,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Midbrain",
        "order": 4,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Amygdala",
        "order": 5,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Choroid plexus",
        "order": 6,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Hippocampal formation",
        "order": 7,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Spinal cord",
        "order": 8,
        "color": "#fcda14",
    },
    {
        "organ": "Brain",
        "tissue": "Retina",
        "order": 9,
        "color": "#fcda14",
    },
    # Endocrine tissues
    {
        "organ": "Endocrine tissues",
        "tissue": "Thyroid gland",
        "order": 10,
        "color": "#755e8f",
    },
    {
        "organ": "Endocrine tissues",
        "tissue": "Parathyroid gland",
        "order": 11,
        "color": "#755e8f",
    },
    {
        "organ": "Endocrine tissues",
        "tissue": "Adrenal gland",
        "order": 12,
        "color": "#755e8f",
    },
    {
        "organ": "Endocrine tissues",
        "tissue": "Pituitary gland",
        "order": 13,
        "color": "#755e8f",
    },
    # Respiratory system
    {
        "organ": "Lung",
        "tissue": "Lung",
        "order": 14,
        "color": "#599c87",
    },
    # Proximal digestive tract
    {
        "organ": "Proximal digestive tract",
        "tissue": "Salivary gland",
        "order": 15,
        "color": "#f3a683",
    },
    {
        "organ": "Proximal digestive tract",
        "tissue": "Esophagus",
        "order": 16,
        "color": "#f3a683",
    },
    {
        "organ": "Proximal digestive tract",
        "tissue": "Tongue",
        "order": 17,
        "color": "#f3a683",
    },
    # Gastrointestinal tract
    {
        "organ": "Gastrointestinal tract",
        "tissue": "Stomach",
        "order": 18,
        "color": "#0072b9",
    },
    {
        "organ": "Gastrointestinal tract",
        "tissue": "Duodenum",
        "order": 19,
        "color": "#0072b9",
    },
    {
        "organ": "Gastrointestinal tract",
        "tissue": "Small intestine",
        "order": 20,
        "color": "#0072b9",
    },
    {
        "organ": "Gastrointestinal tract",
        "tissue": "Colon",
        "order": 21,
        "color": "#0072b9",
    },
    {
        "organ": "Gastrointestinal tract",
        "tissue": "Rectum",
        "order": 22,
        "color": "#0072b9",
    },
    # Liver & Gallbladder
    {
        "organ": "Liver & Gallbladder",
        "tissue": "Liver",
        "order": 23,
        "color": "#cbc3e0",
    },
    {
        "organ": "Liver & Gallbladder",
        "tissue": "Gallbladder",
        "order": 24,
        "color": "#cbc3e0",
    },
    # Pancreas
    {
        "organ": "Pancreas",
        "tissue": "Pancreas",
        "order": 25,
        "color": "#87b985",
    },
    # Kidney & Urinary bladder
    {
        "organ": "Kidney & Urinary bladder",
        "tissue": "Kidney",
        "order": 26,
        "color": "#fd9862",
    },
    {
        "organ": "Kidney & Urinary bladder",
        "tissue": "Urinary bladder",
        "order": 27,
        "color": "#fd9862",
    },
    # Male reproductive system
    {
        "organ": "Male reproductive system",
        "tissue": "Testis",
        "order": 28,
        "color": "#85cdf1",
    },
    {
        "organ": "Male reproductive system",
        "tissue": "Epididymis",
        "order": 29,
        "color": "#85cdf1",
    },
    {
        "organ": "Male reproductive system",
        "tissue": "Seminal vesicle",
        "order": 30,
        "color": "#85cdf1",
    },
    {
        "organ": "Male reproductive system",
        "tissue": "Prostate",
        "order": 31,
        "color": "#85cdf1",
    },
    # Breast & Female reproductive system
    {
        "organ": "Breast & Fefalse reproductive system",
        "tissue": "Vagina",
        "order": 32,
        "color": "#fbb4d2",
    },
    {
        "organ": "Breast & Fefalse reproductive system",
        "tissue": "Ovary",
        "order": 33,
        "color": "#fbb4d2",
    },
    {
        "organ": "Breast & Female reproductive system",
        "tissue": "Fallopian tube",
        "order": 34,
        "color": "#fbb4d2",
    },
    {
        "organ": "Breast & Female reproductive system",
        "tissue": "Endometrium",
        "order": 35,
        "color": "#fbb4d2",
    },
    {
        "organ": "Breast & Female reproductive system",
        "tissue": "Cervix",
        "order": 36,
        "color": "#fbb4d2",
    },
    {
        "organ": "Breast & Female reproductive system",
        "tissue": "Placenta",
        "order": 37,
        "color": "#fbb4d2",
    },
    {
        "organ": "Breast & Female reproductive system",
        "tissue": "Breast",
        "order": 38,
        "color": "#fbb4d2",
    },
    # Muscle tissues
    {
        "organ": "Muscle tissues",
        "tissue": "Heart muscle",
        "order": 39,
        "color": "#ac8165",
    },
    {
        "organ": "Muscle tissues",
        "tissue": "Smooth muscle",
        "order": 40,
        "color": "#ac8165",
    },
    {
        "organ": "Muscle tissues",
        "tissue": "Skeletal muscle",
        "order": 41,
        "color": "#ac8165",
    },
    # Connective & Soft tissue
    {
        "organ": "Connective & Soft tissue",
        "tissue": "Adipose tissue",
        "order": 42,
        "color": "#99d5c6",
    },
    # Skin
    {
        "organ": "Skin",
        "tissue": "Skin",
        "order": 43,
        "color": "#fec3ac",
    },
    # Bone marrow & Lymphoid tissue
    {
        "organ": "Bone marrow & Lymphoid tissue",
        "tissue": "Appendix",
        "order": 44,
        "color": "#df6174",
    },
    {
        "organ": "Bone marrow & Lymphoid tissue",
        "tissue": "Spleen",
        "order": 45,
        "color": "#df6174",
    },
    {
        "organ": "Bone marrow & Lymphoid tissue",
        "tissue": "Lymph node",
        "order": 46,
        "color": "#df6174",
    },
    {
        "organ": "Bone marrow & Lymphoid tissue",
        "tissue": "Tonsil",
        "order": 47,
        "color": "#df6174",
    },
    {
        "organ": "Bone marrow & Lymphoid tissue",
        "tissue": "Bone marrow",
        "order": 48,
        "color": "#df6174",
    },
    {
        "organ": "Bone marrow & Lymphoid tissue",
        "tissue": "Thymus",
        "order": 49,
        "color": "#df6174",
    },
]
