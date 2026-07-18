responses = {

    # ------------------ Greetings ------------------

    r"\b(hi|hello|hey|hii|heyy|good morning|good afternoon|good evening)\b": [
        "Hello! Welcome to the Rule-Based Chatbot. How can I assist you today?",
    ],

    # ------------------ Identity ------------------

    r"\b(who are you|what is your name|your name)\b": [
        "I am a Rule-Based Chatbot developed using Python, Tkinter, Regular Expressions, and Object-Oriented Programming. I answer questions based on predefined rules.",
        "My name is RuleBot. I don't use Artificial Intelligence. Instead, I respond using carefully designed rules and regular expression matching."
    ],

    # ------------------ How are you ------------------

    r"\b(how are you|how are you doing)\b": [
        "I'm doing great! Thank you for asking. How can I help you today?"
    ],
    
    # ------------------ Questions related to technical fields ------------------

    r"\bwhat is python\b": [
        "Python is a high-level, interpreted programming language developed by Guido van Rossum in 1991. It is known for its simple syntax, readability, and powerful libraries. Python is widely used in web development, artificial intelligence, machine learning, data science, automation, cybersecurity, and desktop application development."
    ],

    r"\bpython features\b": [
        "Some important features of Python include:\n\n• Easy to learn and read\n• Object-Oriented Programming support\n• Large standard library\n• Platform independent\n• Open source\n• Dynamically typed\n• Automatic memory management\n• Supports GUI development using Tkinter."
    ],


    r"\bwhat is java\b": [
        "Java is a high-level, object-oriented programming language developed by Sun Microsystems. It follows the principle 'Write Once, Run Anywhere' because Java programs run on the Java Virtual Machine (JVM). Java is widely used for Android apps, enterprise software, web applications, and desktop applications."
    ],


    r"\bwhat is oop\b": [
        "Object-Oriented Programming (OOP) is a programming paradigm based on objects and classes. It helps organize code into reusable components and makes software easier to develop, maintain, and extend."
    ],

    r"\b(four pillars|pillars of oop|oop concepts)\b": [
        "The four pillars of Object-Oriented Programming are:\n\n1. Encapsulation\n2. Inheritance\n3. Polymorphism\n4. Abstraction\n\nThese concepts help create modular, reusable, and maintainable software."
    ],


    r"\bwhat is tkinter\b": [
        "Tkinter is Python's standard GUI (Graphical User Interface) library. It allows developers to create windows, buttons, labels, text boxes, menus, and many other graphical components. It is simple, lightweight, and included with Python."
    ],


    r"\bwhat is regex\b": [
        "Regular Expressions (Regex) are patterns used for searching, matching, and validating text. They are extremely useful for chatbots because they allow a single pattern to match many different user inputs."
    ],

    r"\bwhy regex\b": [
        "Regex allows the chatbot to recognize multiple variations of a question without writing many if-else statements. For example, a single regex can match 'hi', 'hello', or 'hey'."
    ],

    r"\bwhat is chatbot\b": [
        "A chatbot is a software application designed to simulate human conversation. Rule-based chatbots work using predefined rules, while AI chatbots use machine learning and natural language processing to understand user intent."
    ],

    r"\b(rule based chatbot|rule-based chatbot)\b": [
        "A rule-based chatbot responds using predefined rules, keywords, or regular expressions. It does not learn from conversations and can only answer questions that are programmed by the developer."
    ],


    r"\bwhat is ai\b": [
        "Artificial Intelligence (AI) is the branch of computer science that enables machines to perform tasks that normally require human intelligence, such as learning, reasoning, decision making, image recognition, and language understanding."
    ],

    r"\bmachine learning\b": [
        "Machine Learning is a subset of Artificial Intelligence where computers learn from data instead of being explicitly programmed. Machine learning is widely used in recommendation systems, fraud detection, image recognition, and predictive analytics."
    ],


    r"\bwhat is sql\b": [
        "SQL stands for Structured Query Language. It is used to create, retrieve, update, and delete data stored in relational databases like MySQL, PostgreSQL, Oracle, and SQL Server."
    ],

    r"\bwhat is mysql\b": [
        "MySQL is one of the world's most popular relational database management systems. It stores data in tables and uses SQL commands for data management."
    ],


    r"\bwhat is html\b": [
        "HTML stands for HyperText Markup Language. It is the standard language used to create the structure of web pages."
    ],

    r"\bwhat is css\b": [
        "CSS stands for Cascading Style Sheets. It is used to style HTML pages by controlling colors, layouts, fonts, spacing, animations, and responsiveness."
    ],

    r"\bwhat is javascript\b": [
        "JavaScript is a scripting language used to make websites interactive. It can manipulate HTML, validate forms, create animations, and communicate with servers."
    ],


    r"\bwhat is programming\b": [
        "Programming is the process of writing instructions that tell a computer how to perform specific tasks. These instructions are written using programming languages like Python, Java, C++, and JavaScript."
    ],

    r"\bwhat is algorithm\b": [
        "An algorithm is a step-by-step procedure used to solve a problem or perform a computation efficiently."
    ],

    r"\bwhat is data structure\b": [
        "A data structure is a method of organizing and storing data so that it can be accessed and modified efficiently. Examples include arrays, linked lists, stacks, queues, trees, and graphs."
    ],

    # ------------------ Thanks ------------------

    r"\b(thank you|thanks|thx)\b": [
        "You're welcome! I'm always happy to help.",
        "No problem! Feel free to ask another question.",
    ],

    # ------------------ Goodbye ------------------

    r"\b(bye|goodbye|see you|exit|quit)\b": [
        "Goodbye! Thank you for chatting with me. Have a wonderful day!",
        "See you again! "
    ]
}