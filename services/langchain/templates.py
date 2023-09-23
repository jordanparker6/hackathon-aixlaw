CRITISM_SYSTEM_PROMPT = """
Using the following examples please provide a criticism of my current cybersecurity policy :
```
RESPONSIBILITIES
The following are the principal recurring responsibilities of the Cybersecurity Committee. 
1. Information Technology and Network Systems. The Cybersecurity Committee shall oversee
the quality and effectiveness of the Company’s policies and procedures with respect to its
information technology and network systems, including encryption, network security and data
security, as well as access to such systems.
2. IT/Engineering Security Funding. The Cybersecurity Committee shall oversee the Company’s
information technology senior management team relating to budgetary priorities based, in part, on
assessing risk associated with various perceived threats.
3. Incident Response. The Cybersecurity Committee shall review and provide oversight on the
policies and procedures of the Company in preparation for responding to any data security
incidents.
4. Disaster Recovery. The Cybersecurity Committee shall review periodically with management the
Company’s disaster recovery, business continuity, and business resiliency capabilities.
5. Compliance Risks and Audits. The Cybersecurity Committee shall oversee the Company’s
management of internal and external risks related to its information technology systems and 
processes, including encryption, network security, data security, risk management frameworks,
and any internal or third party audits of such systems and processes.
6. Access Controls. The Cybersecurity Committee shall review with management the quality and
effectiveness of IT systems and processes that relate to the Company’s internal access control
systems, including physical, organizational, and technical security.
7. Cyber Insurance. The Cybersecurity Committee shall review the Company’s cyber insurance
policies to ensure appropriate coverage.
8. Product Security. The Cybersecurity Committee shall review periodically with management the
risks related to the security of and access to customer data through use of the Company’s products
and services.



The Committee shall be responsible for the following: 
1. Data Governance – To provide oversight of policies, procedures, plans, and execution intended to provide security, confidentiality, availability, and integrity of the information. 
2. Information Technology Systems – To oversee the quality and effectiveness of the Company’s policies and procedures with respect to its information technology systems, including privacy, network security and data security. 
3. Incident Response – To review and provide oversight on the policies and procedures of the Company in preparation for responding to any material incidents. 
4. Disaster Recovery – To review periodically with management the Company’s disaster recovery capabilities. 
5. Compliance Risks and Internal Audits – To oversee the Company’s management of risks related to its information technology systems and processes, including privacy, network security and data security, and any internal audits of such systems and processes. 
6. Periodic and Annual Reports – To review and oversee the preparation of the Company’s disclosures in its reports filed with the Securities and Exchange Commission relating to the Company’s information technology systems, including privacy, network security, and data security. 
7. IT/Engineering Security Budget – To oversee the Company’s information technology senior management team relating to budgetary priorities based, in part, on assessing risk associated with various perceived threats. 
8. Advisory Role – To review the Company’s information technology strategy or programs relating to new technologies, applications, and systems. 
9. General Authority – To perform such other functions and to have such powers as may be necessary or appropriate in the efficient and lawful discharge of the foregoing.


The Cybersecurity Subcommittee (the “Subcommittee”) of the Audit Committee (the “Committee”) of the Board of Directors of UMH Properties, Inc. (the “Company”) is established to assist the Committee in
fulfilling its oversight responsibilities with respect to the Company’s cybersecurity risks. Company
management is responsible for the preparation, presentation, and self-assessment of the Company’s
cybersecurity policies and practices. The Subcommittee shall be comprised of at least two independent
directors. The Subcommittee shall review and provide high level guidance on cybersecurity-related issues of importance to the Company, including but not limited to:
1. the Company’s cybersecurity policies, procedures, plans, and execution intended to provide
security, confidentiality, availability, and integrity of the information;
2. the Company’s cybersecurity risks, controls and procedures, including high level review of the
threat landscape facing the Company and the Company’s strategy to mitigate cybersecurity risks
and potential breaches, and to ensure legal and regulatory compliance;
3. the recovery and communication plans for any unplanned outage or security breach;
4. data management systems and processes, including security of the Company’s data repositories,
encryption practices, and third-party use of the Company’s customers’ data;
5. periodic reports to the Committee regarding Company systems and processes relating to
cybersecurity; and
6. periodic review of the Company’s IT staffing and cybersecurity employee training plan.


THE COMMITTEE SHALL Review and provide high level guidance on technology related issues of importance to the Company, including but not limited to: 
1. The Company’s technology landscape, competitive assessment and roadmap for future development. 2. The Company’s cybersecurity and other information technology (IT) risks, controls and procedures, including high level review of the threat landscape facing the Company and the Company’s strategy to mitigate cybersecurity risks and potential breaches. The Committee shall also review the recovery and communication plans for any unplanned outage or security breach. 
3. The Company’s technology planning processes to support its growth objectives as well as acquisitions and the system integrations required in support of such activities. 
4. The integrity of the Company’s IT Systems’ operational controls to ensure legal and regulatory compliance. 
5. Data Management Systems & Processes, including security of the Company’s data repositories (US and EU), encryption practices, and third party use of the Company’s customers’ data. 
6. Review the Company’s Cyber insurance policies, if applicable, to ensure appropriate coverage and that all insurance terms and conditions are being met. 
7. With the assistance of Company management, provide an IT Risk Assessment Report to the Board on an annual basis, including systems and processes relating to cybersecurity.
 8. Review the Company’s development and training plan for critical IT staff as well as succession planning and employee training of cybersecurity risks. The Committee shall have the authority to retain outside technical consultants or other appropriate advisors. The Company shall provide for appropriate funding, as determined by the Committee, for payment of compensation to such consultants. The Committee shall review and reassess the adequacy of this Charter periodically and recommend any proposed changes to the Board for approval.
```

At the end of your criticism, say '<END_OF_PLAN>'"
"""

DRAFTING_PROMT = """
Please edit the original text based on the following recommendation by either adding a provision modifying an existant provision.
Please clearly identify the edited section and add a comment about the rationale
---
RECOMMENDATION
{critisim}
---
"""

