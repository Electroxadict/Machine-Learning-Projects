"""
Generate synthetic benchmark and sample datasets for PitchLens AI.
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

SUCCESSFUL_PITCHES = [
    {
        "id": 1,
        "pitch_name": "CloudPulse Analytics",
        "industry": "B2B SaaS",
        "pitch_text": (
            "CloudPulse Analytics is a real-time cloud infrastructure cost optimization platform. "
            "Engineering teams waste over $30B annually on idle cloud resources because existing monitoring tools "
            "lack automated cost-remediation capabilities. CloudPulse solves this with an AI-driven agent that "
            "dynamically resizes Kubernetes clusters and shuts down unused cloud workloads. "
            "Our target market is mid-market DevOps teams with cloud spends over $50,000 per month. The global cloud optimization market is $8.4B TAM. "
            "We operate a B2B SaaS subscription model charging $499 per month per cluster, yielding an 82% gross margin. "
            "We currently have 45 active paying enterprise customers, $28,000 Monthly Recurrent Revenue (MRR), growing 18% MoM, with a 3.2x net LTV/CAC ratio. "
            "Competitors like CloudHealth and Kubecost provide static dashboards, whereas CloudPulse executes automated 1-click resource saving actions with zero downtime. "
            "Our team consists of former AWS senior architects and Stanford computer science graduates with 10+ years of infrastructure experience. "
            "The platform is built on cloud-native serverless architecture capable of scaling to over 10,000 node events per second."
        ),
        "problem": "Engineering teams waste over $30B annually on idle cloud resources due to static monitoring.",
        "solution": "AI-driven automated cost remediation agent for Kubernetes and cloud infrastructure.",
        "market": "$8.4B TAM targeting mid-market DevOps teams with >$50k/mo cloud spend.",
        "business_model": "B2B SaaS subscription at $499/mo per cluster with 82% gross margin.",
        "traction": "45 paying enterprise clients, $28,000 MRR, 18% MoM growth, 3.2x LTV/CAC.",
        "competition": "Competes with CloudHealth & Kubecost by offering automated 1-click remediation vs static dashboards.",
        "team": "Ex-AWS senior architects and Stanford CS alumni with 10+ years infra experience.",
        "scalability": "Cloud-native serverless architecture scaling to 10k+ node events/sec.",
        "presentation_quality": 92,
        "success_label": 1
    },
    {
        "id": 2,
        "pitch_name": "MediSync AI",
        "industry": "HealthTech",
        "pitch_text": (
            "MediSync AI provides automated clinical documentation for primary care physicians. "
            "Doctors spend up to 3 hours every day typing administrative notes into EHR systems, leading to severe clinical burnout and reduced patient face time. "
            "MediSync AI transcribes doctor-patient conversations ambiently and generates HIPAA-compliant medical notes in real time using specialized medical NLP models. "
            "Our addressable market includes 230,000 primary care practices in North America representing a $5.2B SAM. "
            "We charge a recurring SaaS fee of $199 per doctor per month. "
            "We have completed a 6-month clinical pilot across 12 medical clinics, processing 15,000 clinical encounters with a 94% physician satisfaction score and 42% note completion time reduction. "
            "Unlike Nuance DAX or generic dictation software, MediSync integrates natively into EPIC and Cerner workflows without manual copy-pasting. "
            "Founded by a Dr. Elena Vance (MD, Harvard Medical School) and Alex Chen (ex-Google AI Lead). "
            "The system leverages distributed HIPAA-compliant cloud processing to scale effortlessly across hospital networks."
        ),
        "problem": "Doctors spend 3 hours daily on manual EHR notes causing severe burnout.",
        "solution": "Ambient AI transcription converting conversations into real-time EHR notes.",
        "market": "230,000 primary care practices in North America representing $5.2B SAM.",
        "business_model": "SaaS subscription at $199/doctor/month.",
        "traction": "12 clinical pilots, 15,000 encounters processed, 94% satisfaction score.",
        "competition": "Outperforms Nuance DAX via native EPIC/Cerner workflow integration.",
        "team": "MD from Harvard Medical School and former Google AI tech lead.",
        "scalability": "HIPAA-compliant distributed cloud API architecture for enterprise hospital deployment.",
        "presentation_quality": 88,
        "success_label": 1
    },
    {
        "id": 3,
        "pitch_name": "PayFlow Ledger",
        "industry": "FinTech",
        "pitch_text": (
            "PayFlow Ledger automates cross-border B2B invoice settlement for emerging market exporters. "
            "Small businesses in South Asia experience 7 to 14 days payment delays and lose 4% to FX fees when receiving international wire payments. "
            "PayFlow uses instant stablecoin rails and local banking networks to settle cross-border payments in under 60 seconds at a fraction of the cost. "
            "Our market comprises $450B in annual cross-border trade flows between South Asia and North America/Europe. "
            "We monetize via a 0.4% transaction fee per processed invoice, offering 10x savings compared to traditional SWIFT wires. "
            "In 8 months, we have processed ₹4.2 crore ($500,000) in total payment volume across 350 active exporters with zero fraud losses. "
            "Traditional banks take days; PayFlow delivers instant clearance with automated tax and customs compliance documentation. "
            "Led by former Stripe payments engineers and regional banking executives with 15+ combined years in cross-border settlements. "
            "Our API architecture handles multi-currency liquidity routing automatically."
        ),
        "problem": "Exporters suffer 7-14 day payment delays and lose 4% to FX fees on cross-border wires.",
        "solution": "Instant cross-border settlement engine using local banking liquidity and stablecoin rails.",
        "market": "$450B cross-border trade flow between South Asia and US/Europe.",
        "business_model": "0.4% transaction fee per processed invoice.",
        "traction": "Processed ₹4.2 crore ($500,000) volume, 350 active exporters, 0% fraud rate.",
        "competition": "10x cheaper and 100x faster than traditional SWIFT wire transfers.",
        "team": "Ex-Stripe payments engineers and regional banking executives.",
        "scalability": "Automated multi-currency liquidity routing engine supporting 50+ fiat pairs.",
        "presentation_quality": 85,
        "success_label": 1
    },
    {
        "id": 4,
        "pitch_name": "EcoPack Logistics",
        "industry": "CleanTech",
        "pitch_text": (
            "EcoPack Logistics develops reusable bio-composite packaging containers for e-commerce retailers. "
            "Single-use cardboard and plastic packaging generates 14 million tons of landfill waste annually in the US. "
            "EcoPack provides smart, foldable, water-resistant shipping packaging that can be reused up to 50 times with automated return logistics integration. "
            "Targeting D2C fashion and electronics brands in North America, representing a $3.8B sustainable packaging market. "
            "We charge a pay-per-use fee of $0.80 per shipment, saving retailers 20% compared to purchasing new corrugated boxes. "
            "We have signed commercial pilot agreements with 5 mid-size e-commerce brands, shipping over 10,000 packages with an 89% consumer return rate. "
            "Unlike traditional recyclables, EcoPack integrates IoT tracking RFID tags so brands track container return rates in real time. "
            "Co-founded by a materials scientist PhD from MIT and a former VP of Supply Chain at FedEx. "
            "Manufacturing partners in US and Vietnam allow rapid production scale."
        ),
        "problem": "Single-use e-commerce packaging generates 14M tons of landfill waste annually.",
        "solution": "Reusable bio-composite smart shipping containers with IoT return tracking.",
        "market": "D2C fashion and electronics e-commerce packaging market ($3.8B).",
        "business_model": "Pay-per-use shipping fee at $0.80 per cycle.",
        "traction": "5 commercial brand pilots, 10,000 test shipments, 89% return rate.",
        "competition": "Provides integrated RFID tracking vs standard cardboard or basic mailers.",
        "team": "MIT Materials PhD and former VP of Supply Chain at FedEx.",
        "scalability": "Contract manufacturing partnerships capable of 500,000 units/month.",
        "presentation_quality": 80,
        "success_label": 1
    },
    {
        "id": 5,
        "pitch_name": "SkillForge Academy",
        "industry": "EdTech",
        "pitch_text": (
            "SkillForge Academy is an AI-powered adaptive learning platform for corporate software engineering reskilling. "
            "Enterprise tech teams face rapid skill obsolescence, spending $1,200 per employee on generic video courses that yield less than 12% completion rates. "
            "SkillForge creates personalized interactive coding paths with instant AI code review and benchmark assessments. "
            "Our market is the global enterprise IT training market ($28B TAM). "
            "Annual enterprise licensing model charging $350 per developer per year. "
            "We have onboarded 3 fortune 500 corporate clients with 2,500 active software developers and an 84% course completion rate. "
            "Unlike Coursera or Udemy, SkillForge integrates with company GitHub repos to assign real workplace coding projects. "
            "Founded by computer science educators and former EdTech product directors. "
            "The platform architecture automatically updates curriculum based on real-time tech stack trends."
        ),
        "problem": "Generic enterprise video courses have <12% completion rates and waste IT budgets.",
        "solution": "Adaptive AI coding platform with automated PR code reviews and custom company repos.",
        "market": "Global enterprise IT training market ($28B TAM).",
        "business_model": "B2B annual license at $350/developer/year.",
        "traction": "3 Fortune 500 enterprise customers, 2,500 active developer seats, 84% completion rate.",
        "competition": "Real repo integration vs static video lectures like Udemy/Coursera.",
        "team": "Computer science educators and former EdTech product leaders.",
        "scalability": "Scalable cloud IDE sandboxes running on containerized microservices.",
        "presentation_quality": 82,
        "success_label": 1
    },
    {
        "id": 6,
        "pitch_name": "AgriSense IoT",
        "industry": "AgriTech",
        "pitch_text": (
            "AgriSense IoT develops soil sensor probes and satellite predictive analytics for precision agriculture. "
            "Farmers lose 25% of crop yields due to unpredictable soil moisture and over-fertilization. "
            "AgriSense deploys low-cost solar-powered soil sensors paired with satellite imagery algorithms to provide irrigation and fertilizer recommendations via SMS/WhatsApp. "
            "Targeting commercial grain and fruit growers in South Asia and Latin America ($4.1B SAM). "
            "Subscription model charging $15 per acre annually plus hardware cost. "
            "Deployed across 15,000 acres of farmland with 1,200 farmers, demonstrating a 22% yield increase and 18% water savings. "
            "Competitors require expensive cellular gateways; AgriSense uses Long-Range LoRaWAN mesh networks. "
            "Founded by agronomists and IoT hardware engineers. "
            "Sensor hardware is manufactured using modular components for easy field repairs."
        ),
        "problem": "Farmers lose 25% crop yield due to over-irrigation and fertilizer misallocation.",
        "solution": "Low-cost LoRaWAN soil sensors + satellite AI recommendation engine.",
        "market": "Commercial grain/fruit growers in emerging agricultural regions ($4.1B).",
        "business_model": "Hardware sales + $15/acre/year SaaS analytics.",
        "traction": "Deployed across 15,000 acres, 1,200 active farmers, +22% crop yield improvement.",
        "competition": "LoRaWAN mesh network eliminates need for expensive cellular gateways.",
        "team": "Agronomy researchers and IoT hardware engineers.",
        "scalability": "Low-power mesh architecture scalable to millions of connected field acres.",
        "presentation_quality": 78,
        "success_label": 1
    },
    {
        "id": 7,
        "pitch_name": "CyberShield X",
        "industry": "Cybersecurity",
        "pitch_text": (
            "CyberShield X is an autonomous endpoint threat detection platform for SMBs. "
            "Small businesses account for 43% of cyberattacks but cannot afford $150k/year Security Operations Center (SOC) teams. "
            "CyberShield X acts as an automated virtual SOC analyst, isolating ransomware threats in under 5 seconds. "
            "Targeting 6 million North American small-to-midsize businesses ($9.2B TAM). "
            "Monthly subscription of $8 per endpoint per month. "
            "We have secured 1,200 protected endpoints across 40 SMB accounts generating $9,600 MRR. "
            "Unlike traditional antivirus (CrowdStrike, SentinelOne), CyberShield is zero-configuration and managed completely via an automated mobile app. "
            "Founded by former NSA cybersecurity researchers. "
            "Agent footprint is ultra-lightweight (<15MB RAM)."
        ),
        "problem": "43% of cyberattacks target SMBs who lack budget for enterprise SOC teams.",
        "solution": "Autonomous virtual SOC agent for instant endpoint threat isolation.",
        "market": "6 million North American SMBs representing $9.2B TAM.",
        "business_model": "$8 per endpoint per month SaaS model.",
        "traction": "1,200 active endpoints, 40 SMB clients, $9,600 MRR.",
        "competition": "Zero-configuration automated mobile management vs complex enterprise tools.",
        "team": "Former NSA cybersecurity researchers and threat intelligence analysts.",
        "scalability": "Ultra-lightweight endpoint agent (<15MB RAM) with cloud telemetry.",
        "presentation_quality": 84,
        "success_label": 1
    },
    {
        "id": 8,
        "pitch_name": "OmniRetail AI",
        "industry": "E-Commerce",
        "pitch_text": (
            "OmniRetail AI is a dynamic pricing and inventory forecasting engine for Shopify brands. "
            "E-commerce stores lose 15% of annual revenue due to stockouts and unoptimized discounting. "
            "OmniRetail predicts demand spikes using weather, competitor pricing, and historical ad spend, updating prices automatically. "
            "Targeting 1.7M Shopify and WooCommerce merchants ($6.5B SAM). "
            "Revenue share model taking 5% of incremental revenue generated above baseline. "
            "Tested with 25 D2C brands, driving an average revenue boost of +14.2%. "
            "Offers 1-click Shopify app installation vs complex enterprise ERP solutions. "
            "Founded by former Amazon retail algorithms team engineers. "
            "Cloud-native microservices processing millions of pricing sync events daily."
        ),
        "problem": "E-commerce stores lose 15% revenue to stockouts and poor pricing strategies.",
        "solution": "Dynamic AI pricing and demand forecasting engine for e-commerce platforms.",
        "market": "1.7M Shopify & WooCommerce store owners ($6.5B SAM).",
        "business_model": "5% performance fee on incremental revenue uplift.",
        "traction": "25 active brand pilots, +14.2% average merchant revenue increase.",
        "competition": "1-click app store setup vs enterprise ERP pricing suites.",
        "team": "Former Amazon retail algorithm engineers.",
        "scalability": "Cloud microservices capable of processing millions of daily catalog updates.",
        "presentation_quality": 77,
        "success_label": 1
    },
    {
        "id": 9,
        "pitch_name": "QuickDelivery App",
        "industry": "Logistics",
        "pitch_text": (
            "QuickDelivery is an hyper-local grocery delivery app promising delivery in under 30 minutes. "
            "People like getting groceries delivered fast. "
            "We hire gig riders to pick up items from local neighborhood stores and bring them to customers. "
            "Market size is huge because everybody buys groceries every day. "
            "We charge a delivery fee of $3 per order. "
            "We have launched in 1 neighborhood and completed 200 orders so far. "
            "Competitors include Instacart and local delivery boys. "
            "Our team is 2 college students who love food delivery apps. "
            "We plan to expand to 50 cities next year."
        ),
        "problem": "People want fast grocery delivery.",
        "solution": "Gig delivery drivers picking up from local stores.",
        "market": "Huge consumer grocery market.",
        "business_model": "$3 delivery fee per order.",
        "traction": "200 orders completed in 1 neighborhood.",
        "competition": "Competes with Instacart and local delivery services.",
        "team": "2 college student co-founders.",
        "scalability": "Plan to expand to 50 cities next year.",
        "presentation_quality": 45,
        "success_label": 0
    },
    {
        "id": 10,
        "pitch_name": "NextGen VR Classroom",
        "industry": "AR/VR",
        "pitch_text": (
            "NextGen VR Classroom creates 3D virtual reality simulations for high school science labs. "
            "High schools cannot afford physical chemistry and physics laboratory equipment. "
            "We build interactive VR software for Meta Quest headsets allowing students to conduct chemistry experiments safely. "
            "Market size is all high schools in the world. "
            "We hope to charge schools a subscription fee. "
            "We built a prototype physics demo with 3 virtual experiments. "
            "Few competitors exist in this niche. "
            "Team includes VR enthusiasts and software developers. "
            "Hardware requirements require schools to own 30 VR headsets."
        ),
        "problem": "High schools lack budgets for physical science labs.",
        "solution": "Interactive 3D VR science lab simulations.",
        "market": "All global high schools.",
        "business_model": "Subscription fee (pricing not yet determined).",
        "traction": "Prototype physics demo with 3 virtual experiments.",
        "competition": "Few direct competitors in VR high school science labs.",
        "team": "VR enthusiasts and developers.",
        "scalability": "Requires schools to purchase VR headset hardware.",
        "presentation_quality": 52,
        "success_label": 0
    },
    {
        "id": 11,
        "pitch_name": "BioClean Energy",
        "industry": "CleanTech",
        "pitch_text": (
            "BioClean converts agricultural waste into clean hydrogen fuel for commercial trucking fleets. "
            "Diesel trucks contribute 24% of transportation emissions while clean hydrogen remains prohibitively expensive ($14/kg). "
            "BioClean uses proprietary modular thermochemical reactors to produce green hydrogen on-site at $2.80/kg. "
            "Targeting regional trucking logistics hubs ($12B TAM). "
            "We sell fuel under long-term off-take agreements to logistics fleets. "
            "Operating a 1-ton/day pilot facility with $1.2M in contracted off-take commitments from 2 freight operators. "
            "Patented modular catalyst design delivers 3x higher energy efficiency than traditional electrolysis. "
            "Founded by chemical engineering professors and energy sector executives. "
            "Modular reactor units can be deployed directly at fleet depots."
        ),
        "problem": "Diesel trucking accounts for 24% of emissions while green hydrogen is too expensive ($14/kg).",
        "solution": "On-site modular thermochemical reactors producing green hydrogen at $2.80/kg.",
        "market": "Regional trucking hubs and freight depots ($12B TAM).",
        "business_model": "Long-term hydrogen off-take supply agreements.",
        "traction": "1-ton/day pilot plant operating, $1.2M contracted off-take commitments.",
        "competition": "3x higher efficiency patented catalyst vs traditional water electrolysis.",
        "team": "Chemical engineering professors and former energy executives.",
        "scalability": "Standardized containerized reactor units deployed on-site.",
        "presentation_quality": 89,
        "success_label": 1
    },
    {
        "id": 12,
        "pitch_name": "SmartLegal AI",
        "industry": "LegalTech",
        "pitch_text": (
            "SmartLegal AI automates contract review and risk flagging for corporate legal departments. "
            "Corporate legal teams spend 40% of their time manually reviewing standard NDA and vendor contracts, costing companies $120/hour per lawyer. "
            "SmartLegal AI analyzes legal documents against company playbook guidelines, highlighting non-standard risk clauses within 30 seconds. "
            "Targeting mid-sized corporate legal departments ($4.5B SAM). "
            "Tiered annual SaaS subscription starting at $12,000 per legal team per year. "
            "Currently used by 18 enterprise legal teams, analyzing 8,500 contracts with a 91% user retention rate. "
            "Integrates directly into Microsoft Word and Google Docs workflows. "
            "Founded by former corporate attorneys (Harvard Law) and NLP AI researchers. "
            "Enterprise SOC2 certified cloud platform."
        ),
        "problem": "Corporate legal teams waste 40% of time reviewing routine contracts at $120/hr.",
        "solution": "AI contract reviewer flagging non-standard risk clauses against custom playbooks.",
        "market": "Mid-sized corporate legal departments ($4.5B SAM).",
        "business_model": "Annual SaaS licensing starting at $12,000/year.",
        "traction": "18 enterprise legal teams, 8,500 contracts analyzed, 91% retention rate.",
        "competition": "Native MS Word/Google Docs plugin integration vs standalone portals.",
        "team": "Harvard Law attorney co-founders and NLP researchers.",
        "scalability": "SOC2 certified secure cloud architecture with multi-tenant isolation.",
        "presentation_quality": 86,
        "success_label": 1
    },
    {
        "id": 13,
        "pitch_name": "FitLife Mobile",
        "industry": "Health & Fitness",
        "pitch_text": (
            "FitLife Mobile is a workout tracking app with social sharing features. "
            "People find it hard to stay motivated when working out alone. "
            "Our app lets users log exercises and share photos with friends for encouragement. "
            "Target market is anybody who goes to the gym. "
            "We plan to monetize through in-app ads and premium subscriptions. "
            "We have 1,500 free downloads on the App Store. "
            "Competitors include Strava and MyFitnessPal. "
            "Founded by passionate fitness enthusiasts. "
            "App is available on iOS."
        ),
        "problem": "Lack of workout motivation when exercising alone.",
        "solution": "Social workout logger with photo sharing.",
        "market": "Gym goers and fitness enthusiasts.",
        "business_model": "In-app advertisements and premium subscription tier.",
        "traction": "1,500 free app downloads.",
        "competition": "Competes with Strava and MyFitnessPal.",
        "team": "Fitness enthusiasts.",
        "scalability": "Standard mobile application architecture.",
        "presentation_quality": 50,
        "success_label": 0
    },
    {
        "id": 14,
        "pitch_name": "RoboClean Industrial",
        "industry": "Robotics",
        "pitch_text": (
            "RoboClean Industrial manufactures autonomous floor scrubbing robots for commercial warehouses. "
            "Warehouse operators spend $45,000 annually per shift on manual janitorial labor amidst acute labor shortages. "
            "RoboClean's heavy-duty autonomous robots operate continuously for 12 hours using LiDAR navigation and auto-docking water replenishment. "
            "Targeting 40,000 commercial fulfillment centers in North America ($7.8B TAM). "
            "Robotics-as-a-Service (RaaS) subscription model charging $1,800/month per robot including maintenance. "
            "Deployed 32 active robots across 8 logistics hubs, generating $57,600 in Monthly Recurring Revenue with a 14-month hardware payback period. "
            "3D LiDAR SLAM mapping allows setup in under 2 hours without floor markers. "
            "Founded by former iRobot and Tesla Automation robotics engineers. "
            "Modular assembly lines support scalable hardware manufacturing."
        ),
        "problem": "Warehouse operators spend $45k/year on manual cleaning labor amid severe staffing shortages.",
        "solution": "Autonomous commercial heavy-duty floor scrubbing robots with auto-water replenishment.",
        "market": "40,000 North American fulfillment centers ($7.8B TAM).",
        "business_model": "Robotics-as-a-Service (RaaS) subscription at $1,800/month per robot.",
        "traction": "32 active deployed robots, 8 logistics hubs, $57,600 MRR, 14-mo payback.",
        "competition": "2-hour markerless LiDAR SLAM deployment vs complex tape navigation.",
        "team": "Ex-iRobot and Tesla Automation robotics engineers.",
        "scalability": "Modular manufacturing layout scaling to 100 units/month production.",
        "presentation_quality": 90,
        "success_label": 1
    },
    {
        "id": 15,
        "pitch_name": "FinLearn Kids",
        "industry": "EdTech",
        "pitch_text": (
            "FinLearn Kids is a gamified mobile app teaching financial literacy to children aged 8 to 14. "
            "Over 75% of teenagers graduate high school without basic money management skills. "
            "FinLearn offers interactive story games, virtual debit cards, and parent-controlled chore rewards. "
            "Targeting 35 million families in North America ($2.2B SAM). "
            "Subscription of $5.99 per family per month. "
            "Achieved 12,000 monthly active families with a $42,000 Annual Recurrent Revenue (ARR). "
            "Unlike Greenlight, FinLearn focuses heavily on interactive story-based curriculum before issuing real debit cards. "
            "Founded by former elementary educators and fintech product designers. "
            "Scalable cloud architecture integrated with Visa prepaid card processing."
        ),
        "problem": "75% of teens lack basic financial literacy upon graduating high school.",
        "solution": "Gamified financial literacy app with parent-controlled chore rewards and virtual cards.",
        "market": "35 million families in North America ($2.2B SAM).",
        "business_model": "$5.99 per family per month subscription.",
        "traction": "12,000 active families, $42,000 ARR.",
        "competition": "Education-first approach vs pure card management tools like Greenlight.",
        "team": "Elementary educators and fintech product designers.",
        "scalability": "Cloud banking partner integration supporting high transaction volume.",
        "presentation_quality": 81,
        "success_label": 1
    }
]

SAMPLE_PITCHES = [
    {
        "sample_id": "strong_saas",
        "title": "CloudPulse Analytics (Strong Pitch)",
        "pitch_text": SUCCESSFUL_PITCHES[0]["pitch_text"],
        "description": "Complete pitch with strong quantitative metrics, clear business model, and competitive edge."
    },
    {
        "sample_id": "weak_pitch",
        "title": "QuickDelivery App (Weak Pitch)",
        "pitch_text": SUCCESSFUL_PITCHES[8]["pitch_text"],
        "description": "Vague pitch lacking detailed pricing, market evidence, competitive positioning, or clear traction."
    },
    {
        "sample_id": "solution_heavy",
        "title": "QuantumShield Security (Missing Business Model)",
        "pitch_text": (
            "QuantumShield Security develops post-quantum cryptographic encryption keys to protect cloud data centers against future quantum computing attacks. "
            "Current RSA and ECC encryption algorithms will be broken by 1000-qubit quantum computers within 5 years. "
            "QuantumShield provides lattice-based cryptographic algorithms that seamlessly replace standard SSL/TLS certificates. "
            "Targeting enterprise cloud providers and financial institutions. "
            "We have built a working prototype algorithm that runs 40% faster than NIST post-quantum baseline candidates. "
            "Competitors like IBM and Google Quantum are building proprietary systems, but QuantumShield is open-standards compliant. "
            "Founded by quantum physics PhD researchers from Caltech."
        ),
        "description": "Strong technical problem and solution, but missing pricing, monetization model, and financial roadmap."
    },
    {
        "sample_id": "traction_heavy",
        "title": "UrbanRide Scooters (Missing Competition Analysis)",
        "pitch_text": (
            "UrbanRide operates micro-mobility electric scooters for university campuses and suburban business parks. "
            "Students and workers waste time walking 20+ minutes between campus buildings. "
            "UrbanRide deploys docked e-scooters with automated solar charging stations. "
            "Targeting 400 university campuses nationwide ($1.5B TAM). "
            "We charge $1 unlock fee + $0.25 per minute. "
            "In 12 months, we deployed 500 scooters across 3 university campuses, generating $140,000 revenue with over 180,000 completed rides and 14,000 active riders. "
            "Co-founded by mechanical engineers and campus transportation directors. "
            "Modular battery swappable architecture."
        ),
        "description": "Impressive user numbers and revenue, but omits competitive landscape (Bird, Lime, Spin) and differentiation."
    },
    {
        "sample_id": "missing_market",
        "title": "HealthBite Meals (Missing Target Market Details)",
        "pitch_text": (
            "HealthBite Meals delivers pre-portioned organic meals tailored for diabetic patients. "
            "Diabetic patients struggle to prepare low-glycemic meal options, leading to blood sugar spikes and hospitalization. "
            "HealthBite prepares chef-crafted, medically tailored meals delivered weekly to customers' doorsteps. "
            "Subscription model charging $99 per week for 10 meals (65% gross margin). "
            "We have 180 active weekly subscribers generating $17,800 monthly revenue. "
            "Unlike generic meal kits (HelloFresh, Blue Apron), HealthBite meals are certified by clinical dietitians and covered by select health insurance plans. "
            "Founded by a clinical nutritionist and a commercial chef. "
            "Partnered with local commercial kitchens for scalable food prep."
        ),
        "description": "Clear problem, solution, business model, and traction, but lacks quantitative market size (TAM/SAM/SOM)."
    }
]


def generate():
    df_succ = pd.DataFrame(SUCCESSFUL_PITCHES)
    succ_path = DATA_DIR / "successful_pitches.csv"
    df_succ.to_csv(succ_path, index=False)
    print(f"Generated {len(df_succ)} records in {succ_path}")

    df_sample = pd.DataFrame(SAMPLE_PITCHES)
    sample_path = DATA_DIR / "sample_pitches.csv"
    df_sample.to_csv(sample_path, index=False)
    print(f"Generated {len(df_sample)} records in {sample_path}")


if __name__ == "__main__":
    generate()
