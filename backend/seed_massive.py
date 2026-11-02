import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app import models
from app.utils.auth import hash_password

def generate_test_content(db, test_obj):
            reading_section = models.TestSection(
                test_id=test_obj.id,
                section_type=models.SectionType.reading,
                section_number=1,
                title="Reading",
                instructions=(
                    "The Reading test consists of 3 passages with 40 questions. "
                    "You have 60 minutes. Read each passage carefully and answer all questions."
                ),
                time_limit_seconds=3600,
            )
            db.add(reading_section)
            db.commit()
        
            # ── PASSAGE 1: The Growth Mindset ────────────────────────────────────────
            # Questions 1–13 | Types: Matching Headings, T/F/NG, Multiple Choice, Short Answer
        
            passage1 = models.ReadingPassage(
                section_id=reading_section.id,
                passage_number=1,
                title="The Growth Mindset",
                body="""The concept of the 'growth mindset' was developed by psychologist Carol Dweck and introduced in her landmark book 'Mindset: The New Psychology of Success'. It describes the belief that our basic qualities — including intelligence and talents — can be cultivated through effort and dedication. People who have a growth mindset believe that they can get smarter, more talented, and more skilled through hard work and persistence.
        
        In contrast, the 'fixed mindset' refers to the belief that our qualities are fixed and set in stone. People with a fixed mindset believe they were born with certain talents and abilities, and no amount of effort will change that fundamental fact. Such individuals tend to avoid challenges and give up easily when they encounter obstacles.
        
        Research by Dweck and her colleagues has demonstrated that students who hold a growth mindset achieve more than those with a fixed mindset, even when they have lower initial ability. A major focus of the growth mindset in schools is coaxing students away from seeing failure as an indication of their ability, and towards seeing it as a chance to improve.
        
        As educationalist Jeff Howard noted several decades ago: 'Smart is not something that you just are, smart is something that you can get.' This concept has become central to modern educational philosophy and has been adopted by schools and corporations worldwide.
        
        Studies have shown that when students learn about the growth mindset, they show greater motivation in their studies, better grades, and higher achievement scores. Teachers who apply growth mindset principles report more engaged students who are willing to take on challenges and persist through difficulties.
        
        The application of growth mindset theory extends beyond education. In the business world, companies that embrace a growth mindset culture tend to be more innovative, as employees are encouraged to take risks and learn from failures rather than playing it safe to avoid looking incompetent.
        
        However, critics of the growth mindset theory argue that it oversimplifies the complex factors that contribute to achievement, including socioeconomic status, access to resources, and systemic inequalities. They suggest that telling students to simply 'work harder' ignores structural barriers that may prevent them from succeeding regardless of their mindset.
        
        Despite these criticisms, the practical applications of growth mindset research have proven valuable in diverse settings. From rehabilitation programmes for injured athletes to corporate training initiatives, the core message — that ability is not fixed — continues to inspire meaningful change across society.""",
                has_headings=True,
            )
            db.add(passage1)
            db.commit()
        
            # ── QG 1: Matching Headings (Q 1–5) ─────────────────────────────────────
            qg1 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=1,
                question_type=models.QuestionType.match_headings,
                instruction=(
                    "Reading Passage 1 has eight paragraphs, A–H. "
                    "Choose the correct heading for paragraphs A–E from the list of headings below. "
                    "Write the correct number (i–ix) in boxes 1–5 on your answer sheet. "
                    "Note: There are more headings than paragraphs, so you will not use all of them."
                ),
                extra_data={
                    "headings": [
                        "Origins of the theory",                        # i  → A
                        "How fixed beliefs limit potential",            # ii → B
                        "Evidence from classroom research",             # iii → C
                        "A famous quotation on intelligence",           # iv → D
                        "Impact on student performance",                # v  → E
                        "Business applications of the theory",         # vi → F (distractor)
                        "Challenges and criticisms",                    # vii → G (distractor)
                        "The role of government in education",          # viii → distractor
                        "Broader applications across society",          # ix → H (distractor)
                    ]
                },
                order_index=0,
            )
            db.add(qg1)
            db.commit()
        
            for num, prompt, answer in [
                (1,  "Paragraph A",  "i"),
                (2,  "Paragraph B",  "ii"),
                (3,  "Paragraph C",  "iii"),
                (4,  "Paragraph D",  "iv"),
                (5,  "Paragraph E",  "v"),
            ]:
                db.add(models.Question(
                    group_id=qg1.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 2: True / False / Not Given (Q 6–9) ───────────────────────────────
            qg2 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=1,
                question_type=models.QuestionType.true_false_ng,
                instruction=(
                    "Do the following statements agree with the information given in Reading Passage 1? "
                    "Write TRUE, FALSE, or NOT GIVEN in boxes 6–9 on your answer sheet."
                ),
                order_index=1,
            )
            db.add(qg2)
            db.commit()
        
            for num, prompt, answer in [
                (6,  "People with a fixed mindset tend to embrace challenges enthusiastically.", "FALSE"),
                (7,  "Jeff Howard was a student of Carol Dweck.", "NOT GIVEN"),
                (8,  "Companies with growth mindset cultures tend to be more innovative.", "TRUE"),
                (9,  "Critics argue that the growth mindset ignores socioeconomic inequalities.", "TRUE"),
            ]:
                db.add(models.Question(
                    group_id=qg2.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 3: Multiple Choice (Q 10–11) ──────────────────────────────────────
            qg3 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=1,
                question_type=models.QuestionType.multiple_choice,
                instruction="Choose the correct letter, A, B, C or D. Questions 10–11.",
                extra_data={
                    "10": {"options": {
                        "A": "to avoid failure at all costs",
                        "B": "as an opportunity to improve their abilities",
                        "C": "as a measure of their intelligence",
                        "D": "to compare themselves with more successful peers",
                    }},
                    "11": {"options": {
                        "A": "It proves students were born with fixed talent levels.",
                        "B": "Motivation, grades and achievement all improve.",
                        "C": "Only motivation improves, not academic results.",
                        "D": "Students become more competitive but less cooperative.",
                    }},
                },
                order_index=2,
            )
            db.add(qg3)
            db.commit()
        
            for num, prompt, answer in [
                (10, "According to the passage, the growth mindset encourages students to view failure as...", "B"),
                (11, "What does research show happens when students learn about the growth mindset?", "B"),
            ]:
                db.add(models.Question(
                    group_id=qg3.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 4: Short Answer (Q 12–13) ─────────────────────────────────────────
            qg4 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=1,
                question_type=models.QuestionType.short_answer,
                instruction=(
                    "Answer the following questions using NO MORE THAN THREE WORDS from the passage. "
                    "Questions 12–13."
                ),
                order_index=3,
            )
            db.add(qg4)
            db.commit()
        
            for num, prompt, answer, alts in [
                (12, "In what type of publication did Carol Dweck introduce the growth mindset?", "book", ["a book", "her book"]),
                (13, "What do critics say the growth mindset ignores when it tells students to work harder?", "structural barriers", ["socioeconomic status"]),
            ]:
                db.add(models.Question(
                    group_id=qg4.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            print("✅ Passage 1 seeded (Q 1–13, types: Match Headings, T/F/NG, MCQ, Short Answer)")
        
            # ── PASSAGE 2: Ocean Acidification ───────────────────────────────────────
            # Questions 14–26 | Types: Match Paragraph Info, Match Features, Sentence Endings,
            #                           Summary Completion, Table Completion, List of Options
        
            passage2 = models.ReadingPassage(
                section_id=reading_section.id,
                passage_number=2,
                title="Ocean Acidification and Marine Ecosystems",
                body="""A. Since the Industrial Revolution, human activities have released vast quantities of carbon dioxide into the atmosphere. While much attention has focused on the warming of the planet, a quieter but equally significant transformation has been taking place in the world's oceans. The seas absorb approximately 30 percent of the carbon dioxide produced by human activities, and this absorption is altering ocean chemistry in ways that threaten marine life on a colossal scale.
        
        B. When carbon dioxide dissolves in seawater, it forms carbonic acid, which dissociates to release hydrogen ions. This increase in hydrogen ion concentration is precisely what scientists mean by ocean acidification. Since the pre-industrial era, ocean pH has dropped from approximately 8.2 to 8.1 — a seemingly minor shift that in fact represents a 26 percent increase in acidity, given the logarithmic nature of the pH scale.
        
        C. The organisms most immediately affected are those that build shells or skeletons from calcium carbonate — including oysters, mussels, sea urchins, and corals. As acidity rises, the concentration of carbonate ions decreases, making it harder for these creatures to construct and maintain their protective structures. In highly acidic conditions, existing shells can even begin to dissolve.
        
        D. Coral reefs are a particular cause for concern. These ecosystems support approximately 25 percent of all marine species despite covering less than one percent of the ocean floor. Research by marine biologist Dr. Ove Hoegh-Guldberg indicates that at current rates of acidification, conditions may become too hostile for coral reefs to persist beyond the end of this century.
        
        E. However, the effects of ocean acidification are not uniform. Some species of algae and phytoplankton appear to thrive in more acidic conditions. Marine ecologist Dr. Joan Kleypas has documented cases where certain phytoplankton species increase productivity under elevated carbon dioxide levels, potentially altering the composition of marine food webs in unpredictable ways.
        
        F. Scientists are particularly concerned about disruptions to the base of the food chain, which could have cascading consequences throughout entire ecosystems. Zooplankton, which feed on phytoplankton and are themselves consumed by fish, show reduced reproductive success in acidified waters. This weakening of the food chain threatens fisheries that billions of people depend on for protein and livelihoods.
        
        G. Addressing ocean acidification requires a fundamental reduction in carbon dioxide emissions. Unlike some other environmental problems, there are no simple technological fixes currently available at scale. Marine protected areas and reductions in other stressors — such as pollution and overfishing — can improve the resilience of ecosystems, but they cannot reverse acidification itself.
        
        H. Several experimental approaches are being investigated. Ocean alkalinity enhancement involves adding minerals such as limestone to seawater to neutralise acidity. Seaweed farming on a large scale may also help by absorbing carbon dioxide locally. However, experts including oceanographer Dr. Ken Caldeira caution that these methods remain unproven at scale and could introduce unforeseen ecological consequences.""",
                has_headings=True,
            )
            db.add(passage2)
            db.commit()
        
            # ── QG 5: Matching Paragraph Information (Q 14–17) ───────────────────────
            qg5 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=2,
                question_type=models.QuestionType.match_paragraph_info,
                instruction=(
                    "Reading Passage 2 has eight paragraphs, A–H. "
                    "Which paragraph contains the following information? "
                    "Write the correct letter A–H in boxes 14–17. "
                    "NB: You may use any letter more than once."
                ),
                extra_data={"paragraphs": ["A","B","C","D","E","F","G","H"]},
                order_index=4,
            )
            db.add(qg5)
            db.commit()
        
            for num, prompt, answer in [
                (14, "A description of how acidity affects the building materials of certain animals", "C"),
                (15, "A reference to the proportion of ocean floor covered by an important ecosystem", "D"),
                (16, "A mention of species that may benefit from increased acidity", "E"),
                (17, "A warning about dangers to human food supplies", "F"),
            ]:
                db.add(models.Question(
                    group_id=qg5.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 6: Matching Features (Q 18–20) ─────────────────────────────────────
            qg6 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=2,
                question_type=models.QuestionType.match_features,
                instruction=(
                    "Match each finding with the correct researcher. "
                    "Write the correct letter A, B or C in boxes 18–20. "
                    "NB: You may use any letter more than once."
                ),
                extra_data={
                    "categories": {
                        "A": "Dr. Ove Hoegh-Guldberg",
                        "B": "Dr. Joan Kleypas",
                        "C": "Dr. Ken Caldeira",
                    }
                },
                order_index=5,
            )
            db.add(qg6)
            db.commit()
        
            for num, prompt, answer in [
                (18, "Coral reefs may not survive the current century if acidification continues.", "A"),
                (19, "Certain phytoplankton species show increased productivity in high CO₂ conditions.", "B"),
                (20, "Large-scale experimental solutions could have unforeseen ecological consequences.", "C"),
            ]:
                db.add(models.Question(
                    group_id=qg6.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 7: Matching Sentence Endings (Q 21–23) ─────────────────────────────
            qg7 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=2,
                question_type=models.QuestionType.sentence_endings,
                instruction=(
                    "Complete each sentence with the correct ending, A–F, from the box below. "
                    "Write the correct letter in boxes 21–23 on your answer sheet."
                ),
                extra_data={
                    "endings": {
                        "A": "dissolve in highly acidic ocean water.",
                        "B": "thrive under more acidic conditions.",
                        "C": "are already being used successfully to reverse ocean acidification.",
                        "D": "billions of people depend on for food.",
                        "E": "represents a 26 percent increase in acidity.",
                        "F": "cannot be reversed by creating marine protected areas.",
                    }
                },
                order_index=6,
            )
            db.add(qg7)
            db.commit()
        
            for num, prompt, answer in [
                (21, "A drop in ocean pH from 8.2 to 8.1", "E"),
                (22, "The shells of calcium carbonate organisms can", "A"),
                (23, "Fisheries that are threatened by acidification are ones that", "D"),
            ]:
                db.add(models.Question(
                    group_id=qg7.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 8: Summary Completion (Q 24–26) ────────────────────────────────────
            qg8 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=2,
                question_type=models.QuestionType.summary_completion,
                instruction=(
                    "Complete the summary below. "
                    "Choose NO MORE THAN TWO WORDS from the passage for each answer. "
                    "Write your answers in boxes 24–26 on your answer sheet."
                ),
                extra_data={
                    "summary_text": (
                        "Ocean acidification occurs when carbon dioxide dissolves in seawater to form "
                        "[24]. The resulting increase in [25] makes it harder for shell-building organisms "
                        "to survive. Two experimental responses include ocean alkalinity enhancement and "
                        "large-scale [26] farming, though both remain unproven at scale."
                    )
                },
                order_index=7,
            )
            db.add(qg8)
            db.commit()
        
            for num, prompt, answer, alts in [
                (24, "Ocean acidification occurs when CO₂ dissolves in seawater to form ___.", "carbonic acid", None),
                (25, "The resulting increase in ___ makes it harder for shell-building organisms.", "hydrogen ions", ["acidity"]),
                (26, "Two experimental responses include ocean alkalinity enhancement and large-scale ___ farming.", "seaweed", None),
            ]:
                db.add(models.Question(
                    group_id=qg8.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            print("✅ Passage 2 seeded (Q 14–26, types: Match Para, Match Features, Sentence Endings, Summary)")
        
            # ── PASSAGE 3: Vertical Farming ──────────────────────────────────────────
            # Questions 27–40 | Types: Yes/No/NG, Fill in Blank, Note Completion,
            #                           Table Completion, Flow Chart, Diagram Completion,
            #                           List of Options, Choose a Title
        
            passage3 = models.ReadingPassage(
                section_id=reading_section.id,
                passage_number=3,
                title="The Rise of Vertical Farming",
                body="""As the global population continues to grow — with projections suggesting it will reach nearly 10 billion by 2050 — the question of how to feed humanity sustainably has become increasingly urgent. Conventional agriculture already occupies nearly half of the planet's habitable land and accounts for a significant proportion of global greenhouse gas emissions, freshwater consumption, and deforestation.
        
        Against this backdrop, vertical farming has emerged as a promising alternative. The term refers to the practice of growing crops in stacked layers within a controlled environment, typically indoors. By manipulating light, temperature, humidity, and nutrient delivery through hydroponic or aeroponic systems, operators can produce yields many times higher per unit area than conventional fields. Furthermore, because the growing environment is enclosed, crops can be cultivated year-round regardless of seasonal or climatic conditions.
        
        The production process in a vertical farm typically follows a defined sequence. First, seeds are germinated in a sterile nursery environment. Next, seedlings are transferred to growing towers where their roots are misted with nutrient-rich water in aeroponic systems, or submerged in flowing nutrient solution in hydroponic systems. Light-emitting diodes then provide precisely calibrated wavelengths of light to maximise photosynthesis. Finally, the mature crops are harvested, cleaned, and packaged — often within the same building — before being distributed to nearby retailers.
        
        The most compelling argument for vertical farming is its dramatically reduced water usage. Hydroponic systems can use up to 95 percent less water than conventional irrigation, largely because water is recirculated within a closed system rather than lost to evaporation or runoff. In a world where freshwater scarcity is projected to affect billions of people in the coming decades, this efficiency represents a significant advantage.
        
        Proponents also argue that vertical farms, located in or near urban centres, can dramatically shorten supply chains. Produce that travels only a few kilometres from farm to consumer requires far less refrigeration, packaging, and transportation, reducing both costs and carbon emissions.
        
        Despite these advantages, vertical farming faces substantial obstacles. Energy consumption is enormous. A study conducted in 2018 estimated that the energy cost of producing one kilogram of lettuce in a vertical farm could be twenty times higher than in a conventional greenhouse. Unless facilities are powered entirely by renewable energy, the environmental benefits are significantly diminished.
        
        Currently, vertical farming is most economically viable for high-value, fast-growing crops such as leafy greens, herbs, and strawberries. Staple crops like wheat, maize, and rice — which require more land, more light, and generate lower profit margins — remain entirely impractical to grow vertically. The technology must become significantly cheaper and more energy-efficient before it can make a meaningful contribution to global food security.
        
        The diagram below illustrates a cross-section of a typical vertical farm building. The structure features multiple growing floors stacked vertically, with LED lighting arrays positioned above each tier. Water distribution pipes run through the centre of the structure, supplying nutrient solution to growing towers on each level. Air circulation units are mounted at intervals to maintain optimal temperature and humidity throughout the facility.""",
                has_headings=False,
            )
            db.add(passage3)
            db.commit()
        
            # ── QG 9: Yes / No / Not Given (Q 27–30) ─────────────────────────────────
            qg9 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=3,
                question_type=models.QuestionType.yes_no_ng,
                instruction=(
                    "Do the following statements agree with the claims of the writer in Reading Passage 3? "
                    "Write YES, NO, or NOT GIVEN in boxes 27–30 on your answer sheet."
                ),
                order_index=8,
            )
            db.add(qg9)
            db.commit()
        
            for num, prompt, answer in [
                (27, "Vertical farming produces higher yields per unit area than conventional agriculture.", "YES"),
                (28, "Vertical farms near cities eliminate all transportation-related carbon emissions.", "NO"),
                (29, "The 2018 energy study was funded by a government environmental agency.", "NOT GIVEN"),
                (30, "Staple crops like wheat are currently impractical to grow in vertical farms.", "YES"),
            ]:
                db.add(models.Question(
                    group_id=qg9.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── QG 10: Flow Chart Completion (Q 31–33) ────────────────────────────────
            qg10 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=3,
                question_type=models.QuestionType.flow_chart,
                instruction=(
                    "Complete the flow chart below. "
                    "Choose NO MORE THAN TWO WORDS from the passage for each answer. "
                    "Write your answers in boxes 31–33 on your answer sheet."
                ),
                extra_data={
                    "chart_title": "Vertical Farm Production Process",
                    "steps": [
                        "Seeds are germinated in a [31] environment",
                        "↓",
                        "Seedlings are transferred to [32] where nutrients are delivered",
                        "↓",
                        "LEDs provide calibrated light to maximise [33]",
                        "↓",
                        "Crops are harvested, cleaned and packaged on-site",
                        "↓",
                        "Distributed to nearby retailers",
                    ]
                },
                order_index=9,
            )
            db.add(qg10)
            db.commit()
        
            for num, prompt, answer, alts in [
                (31, "Seeds are germinated in a ___ environment.", "sterile nursery", None),
                (32, "Seedlings are transferred to ___ where nutrients are delivered.", "growing towers", None),
                (33, "LEDs provide calibrated light to maximise ___.", "photosynthesis", None),
            ]:
                db.add(models.Question(
                    group_id=qg10.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            # ── QG 11: Table Completion (Q 34–36) ─────────────────────────────────────
            qg11 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=3,
                question_type=models.QuestionType.table_completion,
                instruction=(
                    "Complete the table below. "
                    "Choose NO MORE THAN TWO WORDS AND/OR A NUMBER from the passage for each answer. "
                    "Write your answers in boxes 34–36 on your answer sheet."
                ),
                extra_data={
                    "table_headers": ["Aspect", "Vertical Farming", "Conventional Farming"],
                    "table_rows": [
                        ["Water usage", "Up to [34]% less water used", "Standard irrigation"],
                        ["Energy cost (lettuce)", "[35] times higher per kg", "Baseline"],
                        ["Best-suited crops", "[36], herbs, strawberries", "All crop types"],
                    ]
                },
                order_index=10,
            )
            db.add(qg11)
            db.commit()
        
            for num, prompt, answer, alts in [
                (34, "Hydroponic systems can use up to ___% less water than conventional irrigation.", "95", None),
                (35, "Energy cost of vertical farm lettuce can be ___ times higher than a greenhouse.", "twenty", ["20"]),
                (36, "Vertical farming is currently most viable for ___, herbs, and strawberries.", "leafy greens", None),
            ]:
                db.add(models.Question(
                    group_id=qg11.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            # ── QG 12: Note / Fill-in Blank Completion (Q 37–38) ──────────────────────
            qg12 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=3,
                question_type=models.QuestionType.fill_in_blank,
                instruction=(
                    "Complete the notes below. "
                    "Choose NO MORE THAN TWO WORDS from the passage for each answer. "
                    "Write your answers in boxes 37–38 on your answer sheet."
                ),
                extra_data={
                    "note_title": "Challenges Facing Vertical Farming",
                    "note_text": (
                        "• Enormous [37] consumption limits environmental benefits\n"
                        "• Only viable if powered by [38] energy\n"
                        "• Cannot economically produce staple crops such as wheat or rice"
                    )
                },
                order_index=11,
            )
            db.add(qg12)
            db.commit()
        
            for num, prompt, answer, alts in [
                (37, "Vertical farming faces enormous ___ consumption.", "energy", None),
                (38, "Environmental benefits only realised if powered by ___ energy.", "renewable", None),
            ]:
                db.add(models.Question(
                    group_id=qg12.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            # ── QG 13: Diagram Completion (Q 39) ──────────────────────────────────────
            qg13 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=3,
                question_type=models.QuestionType.diagram_completion,
                instruction=(
                    "Label the diagram of a vertical farm building. "
                    "Choose NO MORE THAN TWO WORDS from the passage for each answer. "
                    "Write your answers in boxes 39 on your answer sheet."
                ),
                extra_data={
                    "diagram_description": (
                        "Cross-section of a vertical farm building showing multiple stacked growing floors. "
                        "Each floor has LED arrays above, growing towers in the middle, and water pipes running through the centre."
                    ),
                    "labels": {
                        "39": "Pipes running through centre of structure that supply nutrient solution",
                    }
                },
                order_index=12,
            )
            db.add(qg13)
            db.commit()
        
            db.add(models.Question(
                group_id=qg13.id, question_number=39,
                prompt="The ___ run through the centre of the structure, supplying nutrient solution to growing towers.",
                correct_answer="water distribution pipes",
                alt_answers=["distribution pipes", "water pipes"],
                order_index=39,
            ))
            db.commit()
        
            # ── QG 14: List of Options / Choose a Title (Q 40) ────────────────────────
            qg14 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=3,
                question_type=models.QuestionType.choose_title,
                instruction=(
                    "Choose the most suitable title for Reading Passage 3 from the list below. "
                    "Write the correct letter A–E in box 40 on your answer sheet."
                ),
                extra_data={
                    "40": {"options": {
                        "A": "The History of Indoor Agriculture",
                        "B": "Vertical Farming: Promise, Process, and Problems",
                        "C": "How to Solve the Global Food Crisis",
                        "D": "Why Conventional Farming Is Becoming Obsolete",
                        "E": "Water Conservation Techniques in Modern Agriculture",
                    }}
                },
                order_index=13,
            )
            db.add(qg14)
            db.commit()
        
            db.add(models.Question(
                group_id=qg14.id, question_number=40,
                prompt="Choose the most suitable title for Reading Passage 3.",
                correct_answer="B",
                order_index=40,
            ))
            db.commit()
        
            print("✅ Passage 3 seeded (Q 27–40, types: Y/N/NG, Flow Chart, Table, Fill Blank, Diagram, Title)")
        
            # ── PASSAGE 4: Noise Pollution (Q 41–43) ──────────────────────────────────
            # Types: summary_completion_select
        
            passage4 = models.ReadingPassage(
                section_id=reading_section.id,
                passage_number=4,
                title="Noise Pollution and Health",
                body="""Noise pollution is increasingly recognised as a significant public health concern. Unlike other forms of pollution, noise is invisible and often transient, which has led to its effects being systematically underestimated. Research over the past two decades has established clear links between chronic noise exposure and a range of health problems including cardiovascular disease, sleep disturbance, and cognitive impairment in children.
        
        The World Health Organization has identified environmental noise as the second most important environmental cause of ill health after air pollution. Studies have shown that individuals living near major roads or airports have significantly higher rates of hypertension and heart attacks. The biological mechanism involves the body's stress response: noise triggers the release of stress hormones such as cortisol, which over time can damage blood vessels and increase cardiovascular risk.
        
        Children are particularly vulnerable to the effects of noise pollution. Research has demonstrated that exposure to aircraft noise impairs reading comprehension and memory development. Even relatively low levels of background noise in classrooms can affect speech perception and attention.
        
        Despite the growing evidence of harm, policy responses have been inconsistent. Many countries lack adequate noise regulations, and enforcement of existing limits remains weak. Urban planning that separates residential areas from noise sources, together with building regulations that require sound insulation, could significantly reduce population exposure.""",
                has_headings=False,
            )
            db.add(passage4)
            db.commit()
        
            # ── QG 15: Summary Completion (Select from list) (Q 41–43) ────────────────
            qg15 = models.QuestionGroup(
                section_id=reading_section.id,
                passage_number=4,
                question_type=models.QuestionType.summary_completion_select,
                instruction=(
                    "Complete the summary below. "
                    "Choose your answers from the list of words and phrases below. "
                    "Write the correct letter A–F in boxes 41–43 on your answer sheet."
                ),
                extra_data={
                    "summary_title": "Effects of Noise Pollution",
                    "summary_text": (
                        "Noise pollution is an [41] environmental health risk. "
                        "Exposure triggers the release of [42], which over time damages blood vessels. "
                        "Children exposed to aircraft noise may suffer impaired [43] development. "
                        "Despite the evidence, policy responses remain [44]."
                    ),
                    "options": {
                        "A": "underestimated",
                        "B": "stress hormones",
                        "C": "readiness",
                        "D": "memory",
                        "E": "cortisol",
                        "F": "visible",
                        "G": "inconsistent",
                    }
                },
                order_index=14,
            )
            db.add(qg15)
            db.commit()
        
            for num, prompt, answer in [
                (41, "Noise pollution is an ___ environmental health risk.", "A"),
                (42, "Exposure triggers the release of ___, which damages blood vessels.", "B"),
                (43, "Children exposed to aircraft noise may suffer impaired ___ development.", "D"),
                (44, "Despite the evidence, policy responses remain ___.", "G"),
            ]:
                db.add(models.Question(
                    group_id=qg15.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            print(f"✅ Passage 4 seeded (Q 41–44, type: summary_completion_select)")
            print(f"✅ Total reading questions seeded: 44")
        
            # ══════════════════════════════════════════════════════════════════════════
            # LISTENING SECTION — 14 question types across 4 recordings (40 Qs)
            # Types: note_completion, short_answer, true_false_ng, multiple_choice,
            #        match_features, sentence_endings, match_paragraph_info,
            #        sentence_completion, table_completion, match_headings,
            #        diagram_labelling, flow_chart, classification, summary_completion
            # ══════════════════════════════════════════════════════════════════════════
            listening_section = models.TestSection(
                test_id=test_obj.id,
                section_type=models.SectionType.listening,
                section_number=1,
                title="Listening",
                instructions="You will hear four recordings and answer 40 questions. You have 30 minutes plus 10 minutes to transfer answers.",
                time_limit_seconds=2400,
                audio_url="/static/audio/test1_listening.mp3",
            )
            db.add(listening_section)
            db.commit()
        
            # ── Recording 1: University Accommodation (Q 1–10) ─────────────────────────
            # Types: note_completion, short_answer, true_false_ng
        
            lqg1 = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.note_completion,
                instruction="Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer. Questions 1–4.",
                order_index=0,
                extra_data={
                    "context": "A student calls the university accommodation office about housing options.",
                    "form_title": "STUDENT ACCOMMODATION ENQUIRY",
                    "form_template": (
                        "**Date:** 14th September\n"
                        "**Student name:** Anna {1}\n"
                        "**Course:** {2}\n"
                        "**Year of study:** {3}\n"
                        "**Preferred hall:** {4} Hall"
                    ),
                    "box_widths": {"1": 140, "2": 180, "3": 80, "4": 140},
                },
            )
            db.add(lqg1)
            db.commit()
        
            for num, prompt, answer, alts in [
                (1, "Student name: Anna ___", "Kowalski", None),
                (2, "Course: ___", "Environmental Science", None),
                (3, "Year of study: ___", "second", ["2nd"]),
                (4, "Preferred hall: ___ Hall", "Gregory", None),
            ]:
                db.add(models.Question(
                    group_id=lqg1.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            lqg1b = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.short_answer,
                instruction="Answer the questions below. Write NO MORE THAN THREE WORDS AND/OR A NUMBER for each answer. Questions 5–7.",
                order_index=1,
                extra_data={"context": "The advisor gives Anna more information about accommodation options."},
            )
            db.add(lqg1b)
            db.commit()
        
            for num, prompt, answer, alts in [
                (5, "How much is the application fee?", "£25", ["25 pounds", "25"]),
                (6, "What type of accommodation does Anna prefer?", "self-catering", None),
                (7, "What should Anna bring for the contract signing?", "passport", ["identification"]),
            ]:
                db.add(models.Question(
                    group_id=lqg1b.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            lqg1c = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.true_false_ng,
                instruction='Do the following statements agree with the information the advisor gives? Write TRUE, FALSE, or NOT GIVEN in boxes 8–10.',
                order_index=2,
                extra_data={"context": "The advisor explains the terms of the accommodation contract."},
            )
            db.add(lqg1c)
            db.commit()
        
            for num, prompt, answer in [
                (8, "The deposit is refundable if Anna gives one month's notice.", "TRUE"),
                (9, "All accommodation halls have private bathrooms.", "FALSE"),
                (10, "International students receive a discount on hall fees.", "NOT GIVEN"),
            ]:
                db.add(models.Question(
                    group_id=lqg1c.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── Recording 2: Technology Museum Tour (Q 11–20) ──────────────────────────
            # Types: multiple_choice, match_features, sentence_endings, match_paragraph_info
        
            lqg2 = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.multiple_choice,
                instruction="Choose the correct letter, A, B, or C. Questions 11–13.",
                extra_data={
                    "context": "A guide shows visitors around the National Museum of Technology.",
                    "11": {"options": {"A": "1978", "B": "1985", "C": "1992"}},
                    "12": {"options": {"A": "Charles Babbage", "B": "Alan Turing", "C": "Ada Lovelace"}},
                    "13": {"options": {"A": "the Model T Ford", "B": "the first telephone", "C": "the first computer"}},
                },
                order_index=3,
            )
            db.add(lqg2)
            db.commit()
        
            for num, prompt, answer in [
                (11, "When was the museum originally opened?", "B"),
                (12, "Who is considered the 'father of computing' according to the guide?", "B"),
                (13, "What is the most popular exhibit on the ground floor?", "B"),
            ]:
                db.add(models.Question(
                    group_id=lqg2.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            lqg2b = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.match_features,
                instruction="Match each invention with its correct inventor. Write the correct letter, A, B, C, or D, in boxes 14–16.",
                extra_data={
                    "context": "The guide describes key inventions and their inventors.",
                    "categories": {
                        "A": "Thomas Edison",
                        "B": "Alexander Graham Bell",
                        "C": "Nikola Tesla",
                        "D": "Guglielmo Marconi",
                    }
                },
                order_index=4,
            )
            db.add(lqg2b)
            db.commit()
        
            for num, prompt, answer in [
                (14, "Light bulb (practical, long-lasting version)", "A"),
                (15, "Radio transmission system", "D"),
                (16, "AC (alternating current) motor", "C"),
            ]:
                db.add(models.Question(
                    group_id=lqg2b.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            lqg2c = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.sentence_endings,
                instruction="Complete each sentence with the correct ending, A–E. Write the correct letter in boxes 17–18.",
                order_index=5,
                extra_data={
                    "context": "The guide talks about the history of the museum building.",
                    "endings": {
                        "A": "was originally a factory.",
                        "B": "was added in 2010.",
                        "C": "housed the city's first telephone exchange.",
                        "D": "was damaged by fire in 1975.",
                        "E": "is now used as an education centre.",
                    }
                },
            )
            db.add(lqg2c)
            db.commit()
        
            for num, prompt, answer in [
                (17, "The main building of the museum", "A"),
                (18, "The east wing of the museum", "C"),
            ]:
                db.add(models.Question(
                    group_id=lqg2c.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            lqg2d = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.match_paragraph_info,
                instruction="Which section of the museum contains the following? Write the correct letter, A, B, C, or D, in boxes 19–20.",
                order_index=6,
                extra_data={
                    "context": "The guide explains the museum's different sections.",
                    "categories": {
                        "A": "Ground Floor — Transport",
                        "B": "First Floor — Communications",
                        "C": "Second Floor — Computing",
                        "D": "Basement — Restoration Workshop",
                    }
                },
            )
            db.add(lqg2d)
            db.commit()
        
            for num, prompt, answer in [
                (19, "A working replica of the first computer", "C"),
                (20, "Antique carriages and early automobiles", "A"),
            ]:
                db.add(models.Question(
                    group_id=lqg2d.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── Recording 3: Business Project Discussion (Q 21–30) ─────────────────────
            # Types: sentence_completion, table_completion, match_headings
        
            lqg3 = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.sentence_completion,
                instruction="Complete the sentences below. Write NO MORE THAN TWO WORDS for each answer. Questions 21–23.",
                order_index=7,
                extra_data={"context": "Two students discuss their business plan project for a startup competition."},
            )
            db.add(lqg3)
            db.commit()
        
            for num, prompt, answer, alts in [
                (21, "Their business idea is a mobile app for finding local ___.", "freelancers", None),
                (22, "The app will use ___ to match users with suitable workers.", "artificial intelligence", ["AI"]),
                (23, "They plan to test the app with ___ users in the first month.", "500", ["five hundred"]),
            ]:
                db.add(models.Question(
                    group_id=lqg3.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            lqg3b = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.table_completion,
                instruction="Complete the table below. Write NO MORE THAN TWO WORDS for each answer. Questions 24–27.",
                order_index=8,
                extra_data={
                    "context": "The students compare three potential app development companies.",
                    "table_headers": ["Company", "Location", "Cost", "Delivery Time"],
                    "table_rows": [
                        ["TechFlow", "Manchester", "£{24}", "6 weeks"],
                        ["AppCraft", "Birmingham", "£12,000", "{25}"],
                        ["Digital {26}", "{27}", "£8,500", "5 weeks"],
                    ],
                    "box_widths": {"24": 80, "25": 80, "26": 120, "27": 130},
                },
            )
            db.add(lqg3b)
            db.commit()
        
            for num, prompt, answer, alts in [
                (24, "TechFlow cost: £___", "9000", ["£9000", "9,000"]),
                (25, "AppCraft delivery time: ___", "8 weeks", None),
                (26, "Third company name: Digital ___", "Solutions", None),
                (27, "Digital Solutions location: ___", "Leeds", None),
            ]:
                db.add(models.Question(
                    group_id=lqg3b.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            lqg3c = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.match_headings,
                instruction="Choose the correct topic heading for each stage of the students' presentation. Write the correct letter, A–E, in boxes 28–30.",
                order_index=9,
                extra_data={
                    "context": "The students outline their presentation structure.",
                    "categories": {
                        "A": "Market research findings",
                        "B": "Financial projections",
                        "C": "Competitor analysis",
                        "D": "Technical development plan",
                        "E": "Marketing and launch strategy",
                    }
                },
            )
            db.add(lqg3c)
            db.commit()
        
            for num, prompt, answer in [
                (28, "Slide 3 — Survey results from 200 potential users", "A"),
                (29, "Slide 5 — Revenue forecast for the first three years", "B"),
                (30, "Slide 7 — Social media campaign and influencer partnerships", "E"),
            ]:
                db.add(models.Question(
                    group_id=lqg3c.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            # ── Recording 4: Coastal Geography Lecture (Q 31–40) ───────────────────────
            # Types: diagram_labelling, flow_chart, classification, summary_completion
        
            lqg4 = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.diagram_labelling,
                instruction="Label the diagram of coastal defences. Write NO MORE THAN TWO WORDS for each answer. Questions 31–33.",
                order_index=10,
                extra_data={
                    "context": "A geography lecturer explains different coastal defence structures.",
                    "diagram_description": "Cross-section of a coastline showing: a tall wall at the top of the beach [31], wooden structures extending into the sea at regular intervals [32], and a pile of rocks at the base of the cliff [33].",
                    "labels": {
                        "31": "Vertical structure built at the back of the beach to prevent flooding",
                        "32": "Wooden barriers built perpendicular to the coastline",
                        "33": "Large rocks placed at the foot of a cliff",
                    }
                },
            )
            db.add(lqg4)
            db.commit()
        
            for num, prompt, answer, alts in [
                (31, "The tall wall at the back of the beach is called a ___.", "sea wall", ["seawall"]),
                (32, "The wooden structures extending into the sea are ___.", "groynes", None),
                (33, "The rock piles at the base of cliffs are known as ___.", "riprap", ["rock armour"]),
            ]:
                db.add(models.Question(
                    group_id=lqg4.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            lqg4b = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.flow_chart,
                instruction="Complete the flow chart below. Write NO MORE THAN TWO WORDS for each answer. Questions 34–36.",
                order_index=11,
                extra_data={
                    "context": "The lecturer describes the process of coastal erosion.",
                    "chart_title": "FORMATION OF A SEA CAVE",
                    "steps": [
                        "Waves attack a weakness in the {34}",
                        "↓",
                        "The crack enlarges through {35} and hydraulic action",
                        "↓",
                        "A {36} is formed as the opening grows larger",
                        "↓",
                        "The cave may eventually become an arch, then a stack"
                    ]
                },
            )
            db.add(lqg4b)
            db.commit()
        
            for num, prompt, answer, alts in [
                (34, "Waves attack a weakness in the ___.", "cliff face", ["cliff"]),
                (35, "The crack enlarges through ___ and hydraulic action.", "abrasion", None),
                (36, "A ___ is formed as the opening grows larger.", "cave", ["sea cave"]),
            ]:
                db.add(models.Question(
                    group_id=lqg4b.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            lqg4c = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.classification,
                instruction="Classify the following coastal management strategies according to the type they belong to. Write the correct letter, A, B, or C, in boxes 37–38.",
                order_index=12,
                extra_data={
                    "context": "The lecturer classifies coastal management approaches.",
                    "categories": {
                        "A": "Hard engineering",
                        "B": "Soft engineering",
                        "C": "Managed retreat",
                    }
                },
            )
            db.add(lqg4c)
            db.commit()
        
            for num, prompt, answer in [
                (37, "Building a concrete sea wall", "A"),
                (38, "Creating artificial sand dunes", "B"),
            ]:
                db.add(models.Question(
                    group_id=lqg4c.id, question_number=num, prompt=prompt,
                    correct_answer=answer, order_index=num,
                ))
            db.commit()
        
            lqg4d = models.QuestionGroup(
                section_id=listening_section.id,
                question_type=models.QuestionType.summary_completion,
                instruction="Complete the summary below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer. Questions 39–40.",
                order_index=13,
                extra_data={
                    "context": "The lecturer summarises the key points about coastal management.",
                    "note_text": (
                        "• Approximately {39}% of the world's coastlines are eroding\n"
                        "• The most sustainable long-term approach is often {40}"
                    )
                },
            )
            db.add(lqg4d)
            db.commit()
        
            for num, prompt, answer, alts in [
                (39, "Approximately ___% of the world's coastlines are eroding.", "70", ["seventy"]),
                (40, "The most sustainable long-term approach is often ___.", "managed retreat", ["retreat"]),
            ]:
                db.add(models.Question(
                    group_id=lqg4d.id, question_number=num, prompt=prompt,
                    correct_answer=answer, alt_answers=alts, order_index=num,
                ))
            db.commit()
        
            # ══════════════════════════════════════════════════════════════════════════
            # WRITING SECTION
            # ══════════════════════════════════════════════════════════════════════════
            writing_section = models.TestSection(
                test_id=test_obj.id,
                section_type=models.SectionType.writing,
                section_number=1,
                title="Writing",
                instructions="Complete both tasks. Task 1: minimum 150 words. Task 2: minimum 250 words.",
                time_limit_seconds=3600,
            )
            db.add(writing_section)
            db.commit()
        
            db.add_all([
                models.WritingTask(
                    section_id=writing_section.id, task_number=1, task_type="task1",
                    prompt="The graph below shows the percentage of households in owned and rented accommodation in England and Wales between 1918 and 2011. Summarise the information by selecting and reporting the main features, and make comparisons where relevant.",
                    image_url="/static/images/task1_graph.png",
                    min_words=150, time_limit_seconds=1200,
                ),
                models.WritingTask(
                    section_id=writing_section.id, task_number=2, task_type="task2",
                    prompt="Write about the following topic:\n\nThe world of work is changing rapidly and employees cannot depend on having the same job or the same working conditions for life.\n\nDiscuss the possible causes for this rapid change, and suggest ways of preparing people for the world of work in the future.\n\nGive reasons for your answer and include any relevant examples from your own knowledge or experience.",
                    min_words=250, time_limit_seconds=2400,
                ),
            ])
            db.commit()
        
            # ══════════════════════════════════════════════════════════════════════════
            # SPEAKING SECTION
            # ══════════════════════════════════════════════════════════════════════════
            speaking_section = models.TestSection(
                test_id=test_obj.id,
                section_type=models.SectionType.speaking,
                section_number=1,
                title="Speaking",
                instructions="The Speaking test has 3 parts. Speak into the microphone for AI scoring.",
                time_limit_seconds=900,
            )
            db.add(speaking_section)
            db.commit()
        
            db.add_all([
                models.SpeakingPart(
                    section_id=speaking_section.id, part_number=1,
                    topic="Personal Introduction",
                    questions=["What is your full name?","Where are you from?","Do you work or study?","What do you do in your free time?"],
                    time_limit_seconds=300,
                ),
                models.SpeakingPart(
                    section_id=speaking_section.id, part_number=2,
                    topic="Describe a person who has influenced you",
                    cue_card="Describe a person who has had a significant influence on your life.\nYou should say:\n• who this person is\n• how you know them\n• how they influenced you\nand explain why they are important to you.\n\nYou have 1 minute to prepare.",
                    questions=["Describe a person who has had a significant influence on your life."],
                    time_limit_seconds=120,
                ),
                models.SpeakingPart(
                    section_id=speaking_section.id, part_number=3,
                    topic="Influence and Role Models",
                    questions=[
                        "Do you think famous people have too much influence on young people today?",
                        "How can parents ensure children have positive role models?",
                        "Has the type of people considered role models changed over the years?",
                    ],
                    time_limit_seconds=300,
                ),
            ])
            db.commit()
        
        

def seed_massive():
    print("Dropping and recreating database...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("Seeding Subscription Plans...")
        db.add_all([
            models.SubscriptionPlan(
                name="Free", plan_type=models.PlanType.free, price_npr=0,
                duration_days=365,
                features=["2 free practice tests", "Basic reading & listening"],
            ),
            models.SubscriptionPlan(
                name="Premium", plan_type=models.PlanType.premium, price_npr=75000,
                duration_days=30,
                features=["All practice tests", "AI Writing feedback", "Progress tracking", "Vocabulary builder"],
            ),
            models.SubscriptionPlan(
                name="Enterprise On Demand", plan_type=models.PlanType.enterprise, price_npr=0,
                duration_days=30,
                features=["Everything in Premium", "Up to 10 premium sub-accounts", "Custom test creation", "Dedicated mentor", "Team analytics", "Priority 24/7 support"],
            ),
        ])
        
        print("Seeding Users...")
        db.add(models.User(
            email="admin@ieltsprep.com", full_name="Admin User",
            hashed_password=hash_password("admin123456"),
            role=models.UserRole.admin, plan=models.PlanType.premium, is_verified=True,
        ))
        db.add(models.User(
            email="demo@ieltsprep.com", full_name="Demo Student",
            hashed_password=hash_password("demo123456"),
            plan=models.PlanType.premium, is_verified=True, target_band=7.5,
        ))
        db.commit()

        print("Seeding Books and Tests (Full Content)...")
        for b_num in range(1, 21):
            print(f"Creating Book {b_num}...")
            book = models.TestBook(
                title=f"Practice Book {b_num}", book_number=b_num,
                test_type=models.TestType.academic,
                description=f"Official IELTS Academic Practice Book {b_num}",
                is_free=(b_num == 1),
            )
            db.add(book)
            db.commit()
            
            for t_num in range(1, 5):
                test = models.IELTSTest(
                    book_id=book.id, test_number=t_num,
                    title=f"Test {t_num} - Book {b_num}",
                    test_type=models.TestType.academic, is_free=(b_num == 1 and t_num == 1),
                )
                db.add(test)
                db.commit()
                
                # Attach full content to this test
                generate_test_content(db, test)
                
        print("✅ Massive Seeding Complete!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_massive()
