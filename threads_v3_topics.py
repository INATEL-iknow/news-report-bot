"""
Threads V3 정의서 - 주제 풀 + 키워드 매핑 (피글맵 진짜 기능 반영)
- 14개 카테고리 정의 항목 모두 포함
- 7가지 진짜 기능만 사용 (가짜 기능 절대 금지)
- 키워드별 다른 기능 매칭
- 톤 일관성 (필러 단어 금지)
"""

# 피글맵 진짜 기능 7가지 (이것 외 절대 사용 금지)
PGLEMAPS_REAL_FEATURES = """
1. Save places you want to visit
2. See all your saved places on one map
3. Organize places into travel itinerary
4. Press "Complete" button to auto-arrange route
5. Check travel distance, transport method, estimated cost
6. Build Day 1, Day 2, Day 3 itinerary flow
7. Manage all places in one place instead of saving separately
"""


# 콘텐츠 유형 정의
POST_TYPES = {
    "controversial": {
        "name_kr": "논쟁형",
        "description": "외국인이 믿고 있는 일반 추천을 흔든다",
    },
    "mistake_warning": {
        "name_kr": "실수 경고형",
        "description": "외국인이 실제로 할 법한 실수를 찌른다",
    },
    "curiosity": {
        "name_kr": "호기심형",
        "description": "본문에서 정답 숨기고 댓글에서 공개",
    },
    "info": {
        "name_kr": "자료 기반 정보형",
        "description": "가격/시간/조건/할인/제도 확실한 정보",
    },
    "route": {
        "name_kr": "동선형",
        "description": "피글맵과 가장 자연스럽게 연결",
    },
}


# 주제 풀 - V3 정의서 + 진짜 기능 매칭
TOPIC_POOL = {
    "HOTEL": {
        "category_name": "Seoul Hotel Area Selection",
        "target_traveler": "first-time visitors who haven't booked yet",
        "what_already_know": "Myeongdong is popular and central",
        "what_dont_know": "Hotel area should match trip type, not popularity",
        "main_hook": "Booking popular hotel areas without checking your itinerary first",
        "post_type": "controversial",
        "comment_1_answer": "Myeongdong only works for shopping/K-beauty/street food trips. For other goals, it's worst for transfers.",
        "comment_2_real_tip": "Cheat sheet matching trip type to hotel area (shopping/nightlife/cafes/clinics/palaces/short trip)",
        "comment_3_real_feature": "Save all the places you want to visit and see them on one map. Then you can see which hotel area sits in the middle of your actual itinerary, not just what's popular.",
        "comment_keyword": "HOTEL",
        "source_needed": "C",
        "forbidden_claims": [
            "Pglemaps recommends hotels",
            "Pglemaps shows nearby places automatically",
            "Real-time hotel booking",
        ],
    },
    
    "ROUTE": {
        "category_name": "Seoul Itinerary Route Planning",
        "target_traveler": "tourists who saved many places but no route",
        "what_already_know": "Saving places on Google Maps is enough",
        "what_dont_know": "Order of places matters more than the list itself",
        "main_hook": "Saving 30 places isn't a travel plan",
        "post_type": "mistake_warning",
        "comment_1_answer": "Seoul neighborhoods look close on map but don't connect well by transit. Wrong order = hours on subway.",
        "comment_2_real_tip": "Group by neighborhood: Gyeongbokgung+Bukchon+Ikseon-dong / Hongdae+Yeonnam / Seongsu+Seoul Forest / Gangnam+Apgujeong",
        "comment_3_real_feature": "Add your saved places, hit the complete button, and the route gets organized for you. You can see travel distance, transport method, and estimated cost for each segment.",
        "comment_keyword": "ROUTE",
        "source_needed": "C",
        "forbidden_claims": [
            "AI generates perfect itinerary",
            "Real-time route optimization",
            "Pglemaps recommends new places",
        ],
    },
    
    "MAP": {
        "category_name": "Korea Map App Confusion",
        "target_traveler": "first-time Korea travelers switching between map apps",
        "what_already_know": "Google Maps works everywhere",
        "what_dont_know": "Korea is one of few countries where multiple map apps are needed",
        "main_hook": "Your Google Maps trip plan won't survive Korea",
        "post_type": "controversial",
        "comment_1_answer": "Google Maps shows limited routes in Korea. Naver/Kakao are local-only. Papago for menus. Switching is exhausting.",
        "comment_2_real_tip": "Use each app for: Google Maps for general search, Naver for directions, Kakao for taxi, Papago for menus",
        "comment_3_real_feature": "Manage all your Korea places in one place instead of saving them separately across Google Maps, Notes app, and screenshots. Everything lives on one map.",
        "comment_keyword": "MAP",
        "source_needed": "C",
        "forbidden_claims": [
            "Auto-translation of Korean places",
            "Built-in taxi calling",
            "Real-time navigation",
        ],
    },
    
    "OLIVEYOUNG": {
        "category_name": "Olive Young Shopping Strategy",
        "target_traveler": "K-beauty shoppers planning last-night shopping",
        "what_already_know": "Olive Young = K-beauty heaven, shop last night",
        "what_dont_know": "Last-night shopping has no backup if items sold out",
        "main_hook": "Last-night Olive Young shopping is how you end up with the wrong stuff",
        "post_type": "mistake_warning",
        "comment_1_answer": "Popular items sell out by branch. Last-night shopping = zero time to check another store or change plans. Luggage space also becomes a problem.",
        "comment_2_real_tip": "Visit mid-trip once for must-haves, compare branches, save last day for small extras. Account for luggage weight.",
        "comment_3_real_feature": "Save Olive Young branches along with the rest of your itinerary, then organize them by day so your shopping fits the natural flow of your trip, not as a panicked last-night stop.",
        "comment_keyword": "OLIVEYOUNG",
        "source_needed": "B",
        "forbidden_claims": [
            "Real-time stock check",
            "Olive Young discount codes",
            "Pglemaps recommends products",
        ],
    },
    
    "GLASSES": {
        "category_name": "Buying Glasses in Korea",
        "target_traveler": "travelers who could benefit from Korean eyewear prices",
        "what_already_know": "Korea has Asian eye exams and glasses",
        "what_dont_know": "Price/quality ratio is exceptional but requires planning",
        "main_hook": "Korea has incredible glasses prices and most travelers miss it",
        "post_type": "curiosity",
        "comment_1_answer": "Production takes 1-3 hours minimum. Tourists who don't plan miss the time window. Some shops require prescriptions you didn't bring.",
        "comment_2_real_tip": "Best time: morning of mid-trip day. Areas: Namdaemun (cheapest), Hongdae (trendy), Gangnam (premium). Bring current glasses or prescription.",
        "comment_3_real_feature": "Save the optical shops you're considering on a map with the rest of your itinerary. You can see distance and transport time between your hotel, the shop, and your next stop.",
        "comment_keyword": "GLASSES",
        "source_needed": "A",
        "forbidden_claims": [
            "Pglemaps recommends specific optical shops",
            "Compare prices and services",
            "Direct booking",
        ],
    },
    
    "CLINIC": {
        "category_name": "Korea Beauty Clinic Planning",
        "target_traveler": "K-beauty tourists with clinic appointments",
        "what_already_know": "Korea is K-beauty paradise",
        "what_dont_know": "Clinic visits eat more time than the appointment slot suggests",
        "main_hook": "Booking K-beauty clinics without planning the rest of the day",
        "post_type": "mistake_warning",
        "comment_1_answer": "Treatments run longer than booked. Recovery time affects rest of day. Wrong location to next stop = lost hours in traffic.",
        "comment_2_real_tip": "Pick clinics in areas you'd visit anyway. Pair with low-effort spots nearby. Block recovery buffer. No packed tour same day.",
        "comment_3_real_feature": "Build your Day 1, Day 2, Day 3 itinerary with the clinic baked in. You can lay out the appointment, recovery time, and gentle follow-up plans on the same day timeline.",
        "comment_keyword": "CLINIC",
        "source_needed": "B",
        "forbidden_claims": [
            "Pglemaps recommends clinics",
            "Real-time appointment booking",
            "Pglemaps shows nearby cafes",
        ],
    },
    
    "HAIR": {
        "category_name": "Korea Hair Salon Visit",
        "target_traveler": "foreigners curious about Korean hair salons",
        "what_already_know": "Korean hair styling is trendy",
        "what_dont_know": "Where you book affects price way more than expected",
        "main_hook": "Tourist-area Korean hair salons can cost 3x the actual local price",
        "post_type": "controversial",
        "comment_1_answer": "Salons in Myeongdong/Hongdae often inflate prices for foreigners. Same service in less touristy areas runs much cheaper.",
        "comment_2_real_tip": "Try less obvious areas: Hapjeong, Yeonnam, Mapo, or Korean-recommended chains. Always confirm price before sitting in chair.",
        "comment_3_real_feature": "Add the salon to your itinerary and see the travel distance and transport from your hotel and next stop, so you're not stuck taking taxis everywhere because the salon location didn't fit your day.",
        "comment_keyword": "HAIR",
        "source_needed": "B",
        "forbidden_claims": [
            "Pglemaps recommends salons",
            "Pre-booking through Pglemaps",
            "Price comparison",
        ],
    },
    
    "HANBOK": {
        "category_name": "Hanbok Rental Decision",
        "target_traveler": "first-time visitors planning palace visits",
        "what_already_know": "Wear Hanbok at Gyeongbokgung for photos",
        "what_dont_know": "Where you rent affects the rest of your day",
        "main_hook": "Most travelers pick a Hanbok rental for the wrong reason",
        "post_type": "mistake_warning",
        "comment_1_answer": "Rental shops near Gyeongbokgung are crowded, pricier, tourist-trap-y. Bukchon shops often better quality, less crowded.",
        "comment_2_real_tip": "Plan: rent in Bukchon, walk to Gyeongbokgung, photos, Bukchon village, Ikseon-dong dinner. Free palace entry with Hanbok.",
        "comment_3_real_feature": "Put the hanbok shop, palace, photo spots, and dinner place on one map. You can see if they actually flow together as one day, not as scattered stops.",
        "comment_keyword": "HANBOK",
        "source_needed": "C",
        "forbidden_claims": [
            "Pglemaps recommends hanbok shops",
            "Pre-booking discounts",
            "Pglemaps shows nearby places",
        ],
    },
    
    "TAXI": {
        "category_name": "Korea Taxi Reality",
        "target_traveler": "first-time Korea travelers assuming taxi is universal",
        "what_already_know": "Take taxi when subway is too far",
        "what_dont_know": "Knowing when NOT to taxi matters more",
        "main_hook": "Defaulting to taxi in Korea quietly burns your money and time",
        "post_type": "mistake_warning",
        "comment_1_answer": "Taxi between scattered neighborhoods is expensive and slow during traffic. Subway often faster and cheaper.",
        "comment_2_real_tip": "Take taxi for: late night, hotel/airport, heavy luggage, short distance. Avoid: cross-city trips during 5-8pm.",
        "comment_3_real_feature": "When you organize your places, you can check travel distance, transport method, and estimated cost between each stop. So you actually see when taxi makes sense and when it doesn't.",
        "comment_keyword": "TAXI",
        "source_needed": "B",
        "forbidden_claims": [
            "Built-in taxi calling",
            "Real-time fare estimates",
            "Pglemaps calls taxi for you",
        ],
    },
    
    "AIRPORT": {
        "category_name": "Incheon Airport Transfer",
        "target_traveler": "arriving travelers without transport plan",
        "what_already_know": "Airport taxi or train to Seoul",
        "what_dont_know": "Choice depends on hotel area, arrival time, and luggage",
        "main_hook": "Defaulting to airport taxi is how you start your Korea trip wrong",
        "post_type": "info",
        "comment_1_answer": "Taxi 60-100k KRW, 60-90min. AREX express 9k KRW, 45min. Limousine bus 17k KRW direct to hotel area.",
        "comment_2_real_tip": "AREX for: Hongdae/Seoul Station area, light luggage. Bus for: direct hotel access. Taxi for: late arrival, heavy luggage, group.",
        "comment_3_real_feature": "Add your hotel and main destinations to your map. You can check the distance and transport options from the airport to your hotel, so the answer is obvious before you land.",
        "comment_keyword": "AIRPORT",
        "source_needed": "A",
        "forbidden_claims": [
            "Pglemaps books airport transfer",
            "Real-time AREX schedule",
            "Pglemaps calls taxi",
        ],
    },
    
    "FOOD": {
        "category_name": "Korean Restaurant Route",
        "target_traveler": "foodies who saved tons of restaurants",
        "what_already_know": "Save TikTok/Instagram restaurants",
        "what_dont_know": "30 saved restaurants don't help if scattered",
        "main_hook": "Saving 30 Korean restaurants doesn't mean you'll actually eat at them",
        "post_type": "mistake_warning",
        "comment_1_answer": "Breakfast, lunch, dinner have different best areas. Scattered restaurants means missed meal times and wrong-area regrets.",
        "comment_2_real_tip": "Group by area and meal time: morning market in Tongin, lunch in Myeongdong area, dinner in Hongdae/Seongsu. Don't backtrack.",
        "comment_3_real_feature": "Organize your saved restaurants into Day 1, Day 2, Day 3 with meal times in mind. You can see if breakfast, lunch, and dinner spots actually fit one day.",
        "comment_keyword": "FOOD",
        "source_needed": "C",
        "forbidden_claims": [
            "Restaurant reservations",
            "Real-time wait times",
            "Pglemaps recommends restaurants",
        ],
    },
    
    "SHOPPING": {
        "category_name": "Seoul Shopping Route",
        "target_traveler": "shopaholics planning Seoul shopping",
        "what_already_know": "Shop at Myeongdong, Dongdaemun, Gangnam",
        "what_dont_know": "Hotel location and luggage decide your real shopping route",
        "main_hook": "Most Seoul shopping plans ignore the actual problem: luggage",
        "post_type": "controversial",
        "comment_1_answer": "Big shopping early in trip means carrying bags. Last-day shopping means no backup. Wrong neighborhood means wasted transfers.",
        "comment_2_real_tip": "Day 1-2: light shopping near hotel. Mid-trip: focused shopping by category. Last day: small items only. Hotel storage helps.",
        "comment_3_real_feature": "When you hit the complete button on your itinerary, the route gets arranged. You can see distance and transport between shopping spots, hotel, and tourist places, so you don't drag bags across the city.",
        "comment_keyword": "SHOPPING",
        "source_needed": "B",
        "forbidden_claims": [
            "Shopping discounts",
            "Tax refund integration",
            "Pglemaps recommends shops",
        ],
    },
    
    "RAIN": {
        "category_name": "Rainy Day Seoul Plan",
        "target_traveler": "travelers worried about weather",
        "what_already_know": "Korea has rainy season in summer",
        "what_dont_know": "Smart travelers prepare backup routes, not just umbrellas",
        "main_hook": "Rainy day in Seoul kills 80% of typical itineraries",
        "post_type": "controversial",
        "comment_1_answer": "Palaces, markets, outdoor photo spots all ruined by rain. Most travelers end up stuck in a hotel cafe or shopping mall.",
        "comment_2_real_tip": "Indoor backup: COEX, Lotte World Mall, Starfield, National Museum, themed cafes. Plan one near each hotel area.",
        "comment_3_real_feature": "Save indoor backup spots along with your outdoor plans on the same map. So when weather changes, you can just rebuild the day with the indoor options already loaded.",
        "comment_keyword": "RAIN",
        "source_needed": "C",
        "forbidden_claims": [
            "Weather forecast integration",
            "Real-time crowd levels",
            "Pglemaps shows nearby places",
        ],
    },
    
    "KOREA": {
        "category_name": "First-Time Korea Travel",
        "target_traveler": "first-time visitors over-planning or under-planning",
        "what_already_know": "Korea is Seoul, food, K-pop, palaces",
        "what_dont_know": "70% planned and 30% flexible is the magic ratio",
        "main_hook": "Your first Korea trip plan is probably broken in one specific way",
        "post_type": "curiosity",
        "comment_1_answer": "Over-planners exhaust themselves. Under-planners waste days deciding. The fix: anchor must-visit places, leave room for discoveries.",
        "comment_2_real_tip": "Plan: 1-2 must-do per day, 1 flexible slot, evenings open. Lock big things (clinics, shows), let small things flow.",
        "comment_3_real_feature": "Manage all your Korea places in one spot instead of having a Notes list, Google Maps stars, and screenshot folder. You can organize them into Day 1, Day 2, Day 3 with travel times shown.",
        "comment_keyword": "KOREA",
        "source_needed": "C",
        "forbidden_claims": [
            "AI itinerary generator",
            "Trip optimization algorithm",
            "Pglemaps suggests places",
        ],
    },
}


def get_all_keywords():
    """모든 키워드 반환"""
    return list(TOPIC_POOL.keys())


def get_topic_config(keyword):
    """키워드의 주제 설정 반환"""
    return TOPIC_POOL.get(keyword, {})


def get_post_type_info(post_type):
    """콘텐츠 유형 정보"""
    return POST_TYPES.get(post_type, {})


def get_random_topics(count=5):
    """랜덤으로 N개 주제 선택 (중복 없음)"""
    import random
    keywords = get_all_keywords()
    
    if count >= len(keywords):
        return keywords
    
    return random.sample(keywords, count)
