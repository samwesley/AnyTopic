import os
from langchain.llms import OpenAI
import openai
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = key

llm = OpenAI(model_name="text-davinci-003", temperature=0)

docs = """The African Space Agency (AfSA) is now a reality and will soon be up and running.

Its headquarters have already taken shape in Egypt's Space City, a sprawling complex of more than 5,000 square metres on the outskirts of Cairo, close to the highway linking the Egyptian capital to the major city of Suez.

Professor Mohamed Belhocine, the African Union's Commissioner for Education, Science, Technology and Innovation, and the Egyptian Minister of Higher Education and Scientific Research, Mohamed Ayman Ahmed Ashour, signed the agreement a few days ago for President Abdel Fattah al-Sisi's government to host the headquarters of the African Space Agency near the pyramids.

PHOTO/African Union - Located on the outskirts of Cairo, the headquarters of the African Space Agency has been built in Egypt's Space City

A new global space player, AfSA is being set up under the umbrella of the African Union (AU), the international organisation based in Addis Ababa, the capital of Ethiopia, which is the forum for dialogue between 55 of the 59 states on the black continent. It is set up, according to article 2 of its constitutive text, to "promote, advise and coordinate the development and use of science, space technologies and associated regulations for the benefit of Africa, the world and inter-African and international cooperation".

Its creation responds to the conviction of most African leaders that space-based applications are key to accelerating the development and prosperity of their respective countries and, step by step, they have brought the African Space Agency into being. The aim is to acquire technologies and build infrastructure to improve, for example, the management of water, marine and terrestrial natural resources, agriculture and the environment.

PHOTO/House of HM the King - During the recent visit of the King and Queen of Spain to Angola, neither the Minister of Foreign Affairs, José Manuel Albares, nor the Secretary of State for Trade, Xiana Méndez, discussed bilateral space cooperation

Angola, another missed opportunity

Nearly fifty satellites of all kinds orbit the Earth under the flags of African countries. The most recent is the 1.9-tonne Angosat-2, a voice, TV and internet communications satellite owned by the government of Angolan President Joao Manuel Gonçalves Lourenço. Manufactured in Russia by the Reshetnev company, it was launched into space on 12 October on a Proton rocket from Russia's Baikonur Cosmodrome. It is the country's first, as AngoSat-1 was lost in December 2017 shortly after its separation from the Zenit-3F rocket.

The King and Queen of Spain have just returned from a three-day state visit to Angola. In the entourage were the Foreign Minister, José Manuel Albares, and the Secretary of State for Trade, Xiana Méndez. But there was no agenda for bilateral space cooperation, despite the fact that the former Portuguese colony has an organisation for this purpose - the National Space Programme Management Office - and the creation of the Spanish Space Agency is imminent. The same thing happened during the visit of President Pedro Sánchez to Kenya and South Africa in October, both nations with space agencies.

The AfSA did not emerge overnight, but has been in the making for more than a decade. AU officials have been in talks for many years with European Space Agency (ESA) managers and technicians to learn about the particularities, structure and functioning of an agency created in 1975 and which does not belong to the European Union.

PHOTO/Roscosmos - Angola's president has a keen interest in the benefits of space. Angosat-1, his first satellite, failed. The second, Angosat-2, is already in orbit for voice, TV and Internet communications

They also met with executives of the latest European Union Space Programme Agency (EUSPA), established by Brussels in April 2021. Headed by Portugal's Rodrigo da Costa, EUSPA is responsible for Europe's satellite navigation programme (Galileo), Earth observation (Copernicus) and government satellite communications (Govsatcom), among others.

As a result of the lessons learned from these contacts, AfSA has similarities and differences with ESA and EUSPA, but in a very different geographical, socio-economic and political environment. China has also played an important role in the founding of the new space actor, given the Asian giant's influence over African countries with agencies, including Egypt, Ethiopia, Nigeria and Sudan.

PHOTO/EU - Since 2018, the African Union has had access to data from the Sentinel observation satellites of the European Union's Copernicus constellation. In the picture, Mahama Ouedraogo and Philippe Brunet representing the two institutions

Consumers of space technologies

AfSA's raison d'être is "to promote and coordinate the implementation of African space policy and strategy, as well as to carry out activities to exploit space technologies and applications for sustainable development and the improvement of the well-being of African citizens", emphasises article 4 of its statutes.

The new agency's role is not to develop satellites, spacecraft, let alone space launchers, initiatives that are at the core of ESA. AfSA has been created to boost the sector in Africa, while also acting as a monitor of progress, both at national and continental level, in line with the African Space Strategy adopted in 2016.

PHOTO/ESA - Most African nations consume satellite communications, meteorology, observation and navigation technologies. But only a few have their own satellites, such as Algeria, Angola, Egypt, Morocco, Nigeria and South Africa

Among the objectives is the interest in "strengthening space missions on the continent to ensure optimal access to space data, information, services and products". It should be noted that, in practice, all African nations are consumers of products derived from satellite communications, meteorology, observation and navigation technologies. Only a few are major players and have satellites of their own: Algeria, Egypt, Morocco, Nigeria and South Africa, joined in recent years by Angola and Kenya.

With the aim of "fostering cooperation and avoiding duplication of efforts", article 5 of the AfSA assigns it the role of "promoting strategic intercontinental partnerships, fostering regional coordination and collaboration, and engaging member states in space-related activities and research in Africa".

PHOTO/African Union - China's penetration of all sectors in Africa is evident. Foreign Minister Qin Gang inaugurated in January the new headquarters of the AU's Centre for Disease Control and Prevention, which uses Beijing satellites

The responsibilities assigned to the Agency also include coordinating the development of a "critical mass of African capabilities in space science, technology and innovation through education and training programmes". It is an extension of the African Space Strategy, which aims to "attract students to postgraduate programmes focused on achieving an indigenous space sector in the changing socio-economic landscape".

AfSA also aims to be the implementing hand for the African Union's self-imposed 2019 space strategy. It is part of the Agenda 2063 adopted by the AU Assembly to make the black continent a "global power of the future". This is what the heads of state and government of the 55 countries proclaim, and they want the African Space Agency to be one of the major tools to achieve this. The steps on paper have been taken, but all are aware that it will not be easy."""

query = "Is the following summary accurate? The African Space Agency (AfSA) is now a reality, with its headquarters located in Egypt's Space City. AfSA was created to promote and coordinate the implementation of African space policy, foster regional coordination and collaboration, as well as attract students to postgraduate programmes focused on achieving an indigenous space sector. It is part of the AU's Agenda 2063 to make Africa a global power of the future."

chain = load_qa_chain(llm, chain_type="stuff")
chain.run(input_documents=docs, question=query)