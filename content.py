"""Everything you read on the Kor website, in English and Bangla side by side.

Edit the words here, then run `python3 build.py`. The build refuses to run if the two languages
have different keys or a different number of list items, so the pages cannot drift apart.

Figures and claims come from the app itself; keep them true to what the app does today (see the status
table in the private app repository's README). The app's source is private, so the site makes no claim
about its licence and links to no repository.
"""

SITE = "https://kor.azimulkabir.com"
DEVELOPER = "https://azimulkabir.com"
EMAIL = "kor@azimulkabir.com"
# The app is not released and its source is private, so the way in is an email, with a subject filled in.
EARLY_ACCESS = {
    "en": "mailto:kor@azimulkabir.com?subject=Kor%20updates",
    "bn": "mailto:kor@azimulkabir.com?subject=%E0%A6%95%E0%A6%B0%20%E0%A6%86%E0%A6%AA%E0%A6%A1%E0%A7%87%E0%A6%9F",
}

# Screenshot names (assets/shots/<lang>/<name>.webp) in the order of the gallery.
GALLERY = ["01-home", "04-tax-detail", "06-wealth-assets", "07-ereturn", "09-calculator"]
HERO_SHOTS = ["09-calculator", "02-home-tiles", "06-wealth-assets"]  # left, middle, right

EN = {
    "lang": "en",
    "name": "Kor",
    "title": "Kor: Bangladesh income tax, worked out as you go",
    "description": "Kor is a private Android app for Bangladesh personal income tax. Record income, investments and tax paid through the year, see what you owe, and get your wealth statement ready. Offline, in English or Bangla.",
    "skip": "Skip to content",
    "nav": {"features": "Features", "screens": "Screens", "privacy": "Privacy", "status": "Status"},
    "switch_label": "Language",
    "switch_to": "বাংলা",
    "hero": {
        "eyebrow": "Bangladesh personal income tax",
        "title": "Know your income tax as you go.",
        "lead": "Kor is a private Android app. Record income, investments and tax paid through the year. See what you owe, how much more you can invest for the rebate before 30 June, and get your wealth statement ready for the e-return.",
        "cta": "Get updates by email",
        "cta2": "See what it does",
        "status": "Pre-alpha, for tax year 2026-27. Kor is not released yet: write to us and we will tell you when it is ready.",
        "chips": ["Works offline", "No account, ads or analytics", "Figures stay on your phone", "English and বাংলা"],
    },
    "glance": {
        "title": "Where you stand, at a glance",
        "body": "The home screen shows what you still owe, how much is already covered by tax deducted at source, and the filing deadline that applies to you, with a checklist of what is left to fill in.",
        "points": [
            "A balance that counts to its new value when you change a figure",
            "A progress ring for tax already paid, and the filing window you are in",
            "A checklist that tells you what is missing, or by how much your wealth statement is out",
        ],
    },
    "features": {
        "title": "What Kor does",
        "items": [
            {
                "title": "Tax worked out, step by step",
                "body": "Slab tax, investment rebate, minimum tax, the net-wealth surcharge and the filing incentive or extra tax, each line in whole taka as the e-return shows it.",
            },
            {
                "title": "A rebate planner",
                "body": "While the income year is open, see how much more to invest by 30 June and exactly what it saves, stopping where minimum tax takes over.",
            },
            {
                "title": "A wealth statement that checks itself",
                "body": "IT-10B and IT-10BB in the e-return's layout, with the same reconciliation NBR applies. Kor tells you whether it balances and, if not, by how much and which way.",
            },
            {
                "title": "An e-return summary",
                "body": "Every figure under its e-return line number. Tap a line to copy its amount, or save the whole summary as a PDF.",
            },
            {
                "title": "A calculator for every amount",
                "body": "Type sums such as 45,000 × 12 on a built-in keypad with lakh grouping. Bangla digits show when the app is in Bangla.",
            },
            {
                "title": "Reminders, only if you want them",
                "body": "A note before the early-filing incentive ends, before extra tax starts or goes up, and before 30 June for investments. Reminders never show an amount.",
            },
        ],
    },
    "screens": {
        "title": "See it in use",
        "note": "Screenshots from the app with made-up figures for a made-up taxpayer.",
        "items": [
            {"title": "Home", "alt": "Kor's home screen: still to pay 32,500 taka of 62,500, with a ring showing 48 percent paid at source, and tiles for salary, other income, rebate and net wealth."},
            {"title": "Tax by slab", "alt": "Your tax screen with a bar splitting income by tax rate, the investment rebate and the filing windows."},
            {"title": "Wealth statement", "alt": "The wealth statement with a ring chart of assets by group and net wealth in the middle."},
            {"title": "E-return summary", "alt": "The e-return summary listing each figure under its e-return line number."},
            {"title": "Calculator keypad", "alt": "The add-income sheet with the calculator keypad open, showing 45,000 times 12."},
        ],
        "hero_alts": [
            "The add-income sheet with the calculator keypad open, showing 45,000 times 12.",
            "Kor's home screen with tiles for salary, other income, rebate and net wealth.",
            "The wealth statement with a ring chart of assets by group.",
        ],
    },
    "privacy": {
        "title": "Your figures never leave your phone",
        "body": "Kor has no internet permission, so it cannot send anything anywhere. Your figures are saved on the phone only, sealed with a key held in Android's Keystore.",
        "points": [
            "No account, no sign-in, no analytics, no advertising, no crash reporting",
            "Excluded from Android backup and device transfer",
            "Notifications only if you turn reminders on, and they never show amounts",
            "Check it yourself: Kor asks for no internet permission, which your phone's app settings show",
        ],
        "link": "Read the privacy policy",
    },
    "status": {
        "title": "What works today, and what does not yet",
        "intro": "Kor is pre-alpha. The rules for tax year 2026-27 (income 1 July 2025 to 30 June 2026, the return filed in late 2026) come from NBR's Income Tax Guide 2026-27, the Finance Act 2026 and the Income Tax Act 2023, and the tests reproduce the guide's worked examples.",
        "works_title": "Works today",
        "works": [
            "Tax-free thresholds for every taxpayer category, and slab tax",
            "Salary by item or as a total, with the employment exemption worked out for you",
            "Other income, investments for rebate, and tax already paid",
            "Net-wealth and luxury surcharge, and minimum tax",
            "When you file: the 30 September incentive and the extra tax from January",
            "The wealth statement (IT-10B) and lifestyle expenses (IT-10BB)",
            "The e-return summary, copy by line, and PDF export",
            "Opt-in deadline reminders, in English or Bangla",
        ],
        "later_title": "Not yet",
        "later": [
            "Capital gains and other reduced-rate or final-settlement income",
            "Environmental surcharge",
            "Tax years other than 2026-27",
            "Encrypted export and import, for a new phone",
            "Importing from Actua and Actual Budget",
            "More than one taxpayer on one phone",
        ],
        "link": "Tell us what you need",
    },
    "footer": {
        "disclaimer": "Kor is an independent tool and is not affiliated with the National Board of Revenue (NBR). It helps you prepare figures; it is not tax advice. Check your return against the Income Tax Act 2023, the Finance Act for the year and NBR guidance before filing.",
        "made": "Made by Azimul Kabir Apu",
        "contact": "Contact",
        "developer": "Developer's website",
        "privacy": "Privacy policy",
    },
    "privacy_page": {"title": "Kor privacy policy", "back": "Back to the home page"},
    "notfound": {"title": "Page not found", "body": "That page does not exist. The home page has everything.", "link": "Go to the home page"},
}

BN = {
    "lang": "bn",
    "name": "কর",
    "title": "কর (Kor): বাংলাদেশের আয়কর, বছরজুড়ে হিসাব",
    "description": "কর (Kor) বাংলাদেশের ব্যক্তিগত আয়করের জন্য একটি ব্যক্তিগত অ্যান্ড্রয়েড অ্যাপ। বছরজুড়ে আয়, বিনিয়োগ ও পরিশোধিত কর লিখে রাখুন, দেখুন কত কর দিতে হবে, আর সম্পদ বিবরণী তৈরি রাখুন। অফলাইনে চলে, বাংলা ও ইংরেজিতে।",
    "skip": "মূল অংশে যান",
    "nav": {"features": "সুবিধা", "screens": "স্ক্রিন", "privacy": "গোপনীয়তা", "status": "অবস্থা"},
    "switch_label": "ভাষা",
    "switch_to": "English",
    "hero": {
        "eyebrow": "বাংলাদেশের ব্যক্তিগত আয়কর",
        "title": "বছরজুড়ে জানুন, আয়কর কত।",
        "lead": "কর একটি ব্যক্তিগত অ্যান্ড্রয়েড অ্যাপ। বছরের মধ্যেই আয়, বিনিয়োগ ও পরিশোধিত কর লিখে রাখুন। দেখুন কত কর দিতে হবে, ৩০ জুনের আগে রেয়াতের জন্য আর কত বিনিয়োগ করা যায়, আর ই-রিটার্নের জন্য সম্পদ বিবরণী তৈরি রাখুন।",
        "cta": "ইমেইলে খবর পান",
        "cta2": "কী কী করে দেখুন",
        "status": "প্রি-আলফা, করবর্ষ ২০২৬-২৭ এর জন্য। কর এখনো প্রকাশিত হয়নি: আমাদের লিখুন, তৈরি হলে জানাব।",
        "chips": ["অফলাইনে চলে", "অ্যাকাউন্ট, বিজ্ঞাপন বা অ্যানালিটিক্স নেই", "হিসাব থাকে আপনার ফোনেই", "বাংলা ও English"],
    },
    "glance": {
        "title": "এক নজরে আপনার অবস্থান",
        "body": "হোম স্ক্রিনে দেখা যায় আপনার আর কত কর বাকি, উৎসে কর্তনে কতটা মেটানো হয়েছে, আপনার জন্য কোন দাখিলের সময় প্রযোজ্য, সঙ্গে কী কী পূরণ করা বাকি তার চেকলিস্ট।",
        "points": [
            "কোনো অঙ্ক বদলালে ব্যালেন্স নতুন মানে গুনে গুনে পৌঁছায়",
            "পরিশোধিত করের জন্য একটি অগ্রগতির বৃত্ত, আর আপনি যে দাখিলের সময়ে আছেন তা",
            "চেকলিস্টে দেখা যায় কী বাকি, অথবা সম্পদ বিবরণী কত অমিল",
        ],
    },
    "features": {
        "title": "কর কী কী করে",
        "items": [
            {
                "title": "ধাপে ধাপে কর হিসাব",
                "body": "ধাপভিত্তিক কর, বিনিয়োগ রেয়াত, ন্যূনতম কর, নিট সম্পদের উপর সারচার্জ এবং দাখিলের প্রণোদনা বা অতিরিক্ত কর। প্রতিটি লাইন ই-রিটার্নের মতো পূর্ণ টাকায়।",
            },
            {
                "title": "রেয়াত পরিকল্পনা",
                "body": "আয়বর্ষ চলাকালে দেখুন ৩০ জুনের মধ্যে আর কত বিনিয়োগ করলে ঠিক কত কর কমে। যেখানে ন্যূনতম কর শুরু হয়, সেখানেই থামে।",
            },
            {
                "title": "নিজে যাচাই হওয়া সম্পদ বিবরণী",
                "body": "ই-রিটার্নের বিন্যাসে আইটি-১০বি ও আইটি-১০বিবি, এনবিআর যেভাবে মিলিয়ে দেখে সেভাবেই। মিললে কর জানায়, না মিললে কত এবং কোন দিকে ফারাক তা বলে।",
            },
            {
                "title": "ই-রিটার্ন সারাংশ",
                "body": "প্রতিটি অঙ্ক ই-রিটার্নের লাইন নম্বরের নিচে। কোনো লাইনে ট্যাপ করলে অঙ্ক কপি হয়, অথবা পুরো সারাংশ পিডিএফ হিসেবে সংরক্ষণ করুন।",
            },
            {
                "title": "প্রতিটি অঙ্কের জন্য ক্যালকুলেটর",
                "body": "লাখ-কোটির কমাসহ কিপ্যাডে ৪৫,০০০ × ১২-এর মতো যোগ-গুণ লিখুন। অ্যাপ বাংলায় থাকলে অঙ্ক বাংলায় দেখায়।",
            },
            {
                "title": "সময়ের স্মরণ, চাইলে",
                "body": "আগাম দাখিলের প্রণোদনা শেষ হওয়ার আগে, অতিরিক্ত কর শুরু বা বাড়ার আগে এবং বিনিয়োগের জন্য ৩০ জুনের আগে একটি বার্তা। কোনো অঙ্ক দেখানো হয় না।",
            },
        ],
    },
    "screens": {
        "title": "ব্যবহারে দেখুন",
        "note": "কাল্পনিক করদাতার কাল্পনিক অঙ্ক দিয়ে অ্যাপ থেকে নেওয়া স্ক্রিনশট।",
        "items": [
            {"title": "হোম", "alt": "করের হোম স্ক্রিন: ৬২,৫০০ টাকার মধ্যে ৩২,৫০০ টাকা বাকি, উৎসে ৪৮ শতাংশ পরিশোধের বৃত্ত, এবং বেতন, অন্যান্য আয়, রেয়াত ও নিট সম্পদের টাইল।"},
            {"title": "ধাপ অনুযায়ী কর", "alt": "আপনার কর স্ক্রিন: করের হার অনুযায়ী আয়ের বিভাজনের বার, বিনিয়োগ রেয়াত এবং দাখিলের সময়।"},
            {"title": "সম্পদ বিবরণী", "alt": "সম্পদ বিবরণী: গ্রুপ অনুযায়ী সম্পদের বৃত্ত চার্ট, মাঝখানে নিট সম্পদ।"},
            {"title": "ই-রিটার্ন সারাংশ", "alt": "ই-রিটার্ন সারাংশ: প্রতিটি অঙ্ক তার ই-রিটার্ন লাইন নম্বরসহ।"},
            {"title": "ক্যালকুলেটর কিপ্যাড", "alt": "আয় যোগ করার শিট, ক্যালকুলেটর কিপ্যাড খোলা, ৪৫০০০ × ১২ লেখা।"},
        ],
        "hero_alts": [
            "আয় যোগ করার শিট, ক্যালকুলেটর কিপ্যাড খোলা, ৪৫০০০ × ১২ লেখা।",
            "করের হোম স্ক্রিন: বেতন, অন্যান্য আয়, রেয়াত ও নিট সম্পদের টাইল।",
            "সম্পদ বিবরণী: গ্রুপ অনুযায়ী সম্পদের বৃত্ত চার্ট।",
        ],
    },
    "privacy": {
        "title": "আপনার হিসাব কখনো ফোন ছাড়ে না",
        "body": "করের ইন্টারনেট অনুমতি নেই, তাই কোথাও কিছু পাঠাতে পারে না। আপনার হিসাব শুধু ফোনেই থাকে, অ্যান্ড্রয়েড কিস্টোরের চাবিতে সিল করা।",
        "points": [
            "অ্যাকাউন্ট, সাইন-ইন, অ্যানালিটিক্স, বিজ্ঞাপন বা ক্র্যাশ রিপোর্টিং নেই",
            "অ্যান্ড্রয়েড ব্যাকআপ ও ডিভাইস ট্রান্সফার থেকে বাদ",
            "নোটিফিকেশন শুধু আপনি স্মরণ চালু করলে, আর তাতে কোনো অঙ্ক দেখানো হয় না",
            "নিজে যাচাই করুন: কর ইন্টারনেট অনুমতি চায় না, আপনার ফোনের অ্যাপ সেটিংসেই তা দেখা যায়",
        ],
        "link": "গোপনীয়তা নীতি পড়ুন",
    },
    "status": {
        "title": "আজ কী চলে, আর কী এখনো নয়",
        "intro": "কর এখনো প্রি-আলফা। করবর্ষ ২০২৬-২৭ এর নিয়ম (আয় ১ জুলাই ২০২৫ থেকে ৩০ জুন ২০২৬, রিটার্ন ২০২৬ সালের শেষে) নেওয়া হয়েছে এনবিআরের আয়কর নির্দেশিকা ২০২৬-২০২৭, অর্থ আইন ২০২৬ ও আয়কর আইন ২০২৩ থেকে, আর টেস্টে নির্দেশিকার উদাহরণগুলো মেলানো হয়।",
        "works_title": "আজ যা চলে",
        "works": [
            "প্রতিটি করদাতা শ্রেণির করমুক্ত সীমা ও ধাপভিত্তিক কর",
            "বেতন খাতওয়ারি বা মোট হিসেবে, চাকরির অব্যাহতি আপনার হয়ে হিসাব করা",
            "অন্যান্য আয়, রেয়াতের জন্য বিনিয়োগ এবং পরিশোধিত কর",
            "নিট সম্পদ ও বিলাসিতার সারচার্জ এবং ন্যূনতম কর",
            "দাখিলের সময়: ৩০ সেপ্টেম্বরের প্রণোদনা এবং জানুয়ারি থেকে অতিরিক্ত কর",
            "সম্পদ বিবরণী (আইটি-১০বি) ও জীবনযাপন সংক্রান্ত ব্যয় (আইটি-১০বিবি)",
            "ই-রিটার্ন সারাংশ, লাইন ধরে কপি এবং পিডিএফ",
            "ইচ্ছামতো চালু করা সময়ের স্মরণ, বাংলা বা ইংরেজিতে",
        ],
        "later_title": "এখনো নয়",
        "later": [
            "মূলধনি আয় এবং অন্যান্য হ্রাসকৃত হার বা চূড়ান্ত নিষ্পত্তির আয়",
            "পরিবেশ সারচার্জ",
            "২০২৬-২৭ ছাড়া অন্য করবর্ষ",
            "নতুন ফোনের জন্য এনক্রিপ্টেড এক্সপোর্ট ও ইমপোর্ট",
            "Actua ও Actual Budget থেকে ইমপোর্ট",
            "এক ফোনে একাধিক করদাতা",
        ],
        "link": "আপনার কী দরকার জানান",
    },
    "footer": {
        "disclaimer": "কর একটি স্বাধীন টুল, জাতীয় রাজস্ব বোর্ডের (এনবিআর) সঙ্গে এর কোনো সম্পর্ক নেই। এটি হিসাব তৈরিতে সাহায্য করে; এটি কর পরামর্শ নয়। দাখিলের আগে আপনার রিটার্ন আয়কর আইন ২০২৩, সংশ্লিষ্ট বছরের অর্থ আইন ও এনবিআরের নির্দেশনার সঙ্গে মিলিয়ে নিন।",
        "made": "তৈরি করেছেন আজিমুল কবির আপু",
        "contact": "যোগাযোগ",
        "developer": "ডেভেলপারের ওয়েবসাইট",
        "privacy": "গোপনীয়তা নীতি",
    },
    "privacy_page": {"title": "কর গোপনীয়তা নীতি", "back": "হোম পাতায় ফিরুন"},
    "notfound": {"title": "পাতাটি পাওয়া যায়নি", "body": "এই পাতাটি নেই। হোম পাতায় সবকিছু আছে।", "link": "হোম পাতায় যান"},
}
