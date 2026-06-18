"""
Threads V3 정의서 - 주제 풀 + 키워드 매핑 (V3 완전 반영)
- V3 정의서 13장 14개 항목 모두 포함
- 5가지 콘텐츠 유형
- 본문 반응 유도 트리거
- 입점 전/후 구분 (안경점)
"""

# 콘텐츠 유형 정의 (V3 정의서 11장)
POST_TYPES = {
    "controversial": {
        "name_kr": "논쟁형",
        "description": "외국인이 믿고 있는 일반 추천을 흔든다",
        "examples": [
            "Myeongdong is not always the best place to stay",
            "First-time visitors overrate Gangnam",
        ],
    },
    "mistake_warning": {
        "name_kr": "실수 경고형",
        "description": "외국인이 실제로 할 법한 실수를 찌른다",
        "examples": [
            "Don't do Olive Young shopping on last night",
            "Don't book hotel before checking route",
        ],
    },
    "curiosity": {
        "name_kr": "호기심형",
        "description": "본문에서 정답 숨기고 댓글에서 공개",
        "examples": [
            "Most tourists skip one smart thing to buy in Korea",
            "There's one Seoul mistake that wastes half your day",
        ],
    },
    "info": {
        "name_kr": "자료 기반 정보형",
        "description": "가격/시간/조건/할인/제도 확실한 정보",
        "examples": [
            "Korea glasses price range",
            "Airport train vs taxi",
        ],
    },
    "route": {
        "name_kr": "동선형",
        "description": "피글맵과 가장 자연스럽게 연결",
        "examples": [
            "Hongdae + Seongsu + Gangnam in one day",
            "Rainy day Seoul route",
        ],
    },
}


# 주제 풀 - V3 정의서 13장 14개 항목 완전 반영
TOPIC_POOL = {
    "HOTEL": {
        "category_id": "hotel",
        "category_name": "Seoul Hotel Area Selection",
        "target_traveler": "first-time visitors who haven't booked yet",
        "what_foreigners_already_know": "Myeongdong is popular and 'central'",
        "what_foreigners_do_not_know": "Hotel area should match trip type, not popularity",
        "main_hook": "Staying in popular areas can ruin your trip if it doesn't match your itinerary",
        "controversy_or_curiosity": "controversy",
        "post_type": "controversial",
        "comment_1_answer": "Myeongdong only works for shopping/K-beauty/street food trips. For other goals, it's worst for transfers.",
        "comment_2_real_tip": "Cheat sheet matching trip type to hotel area (shopping/nightlife/cafes/clinics/palaces/short trip)",
        "comment_3_pglemaps_benefit": "Save all your places on one map first, then see which hotel area fits your itinerary",
        "comment_keyword": "HOTEL",
        "source_needed": "C",  # C급 (자료 불필요)
        "current_or_future_feature": "current",
        "forbidden_claims": ["Pglemaps recommends hotels", "Real-time hotel booking", "Hotel price comparison"],
    },
    
    "ROUTE": {
        "category_id": "route",
        "category_name": "Seoul Itinerary Route Planning",
        "target_traveler": "tourists who have saved many places but no route",
        "what_foreigners_already_know": "Saving places on Google Maps is enough",
        "what_foreigners_do_not_know": "Order of places matters more than the list itself",
        "main_hook": "Saving 30 places isn't a travel plan",
        "controversy_or_curiosity": "curiosity",
        "post_type": "mistake_warning",
        "comment_1_answer": "Seoul neighborhoods look close on map but don't connect well by transit. Wrong order = hours on subway.",
        "comment_2_real_tip": "Group places by neighborhood: Gyeongbokgung+Bukchon+Ikseon-dong / Hongdae+Yeonnam / Seongsu+Seoul Forest / Gangnam+Apgujeong",
        "comment_3_pglemaps_benefit": "Put saved places on one map and check travel flow before arriving",
        "comment_keyword": "ROUTE",
        "source_needed": "C",
        "current_or_future_feature": "current",
        "forbidden_claims": ["AI generates perfect itinerary", "Real-time route optimization"],
    },
    
    "MAP": {
        "category_id": "map",
        "category_name": "Korea Map App Confusion",
        "target_traveler": "first-time Korea travelers switching between map apps",
        "what_foreigners_already_know": "Google Maps works everywhere",
        "what_foreigners_do_not_know": "Korea is one of few countries where multiple map apps are needed",
        "main_hook": "Your Google Maps trip plan won't survive Korea",
        "controversy_or_curiosity": "controversy",
        "post_type": "controversial",
        "comment_1_answer": "Google Maps shows limited routes in Korea. Naver/Kakao are local-only. Papago for menus. Switching is exhausting.",
        "comment_2_real_tip": "Use each app for: Google Maps for saving, Naver for directions, Kakao for taxi, Papago for menus",
        "comment_3_pglemaps_benefit": "Organize saved places on one map without switching apps",
        "comment_keyword": "MAP",
        "source_needed": "C",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Auto-translation of all Korean places", "Built-in taxi calling"],
    },
    
    "OLIVEYOUNG": {
        "category_id": "oliveyoung",
        "category_name": "Olive Young Shopping Strategy",
        "target_traveler": "K-beauty shoppers planning last-night shopping",
        "what_foreigners_already_know": "Olive Young = K-beauty heaven, shop last night",
        "what_foreigners_do_not_know": "Last-night shopping has no backup if items sold out",
        "main_hook": "Don't save Olive Young for your last night",
        "controversy_or_curiosity": "curiosity",
        "post_type": "mistake_warning",
        "comment_1_answer": "Popular items sell out by branch. Last-night shopping = zero time to check another store or change plans.",
        "comment_2_real_tip": "Visit mid-trip once for must-haves, compare branches, use last day only for small extras. Also watch luggage space.",
        "comment_3_pglemaps_benefit": "Save Olive Young branches with shopping streets, cafes, tourist spots together to check if route fits",
        "comment_keyword": "OLIVEYOUNG",
        "source_needed": "B",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Real-time stock check", "Olive Young discount codes"],
    },
    
    "GLASSES": {
        "category_id": "glasses",
        "category_name": "Buying Glasses in Korea",
        "target_traveler": "travelers who could benefit from Korean eyewear prices",
        "what_foreigners_already_know": "Korea has Asian eye exams and glasses",
        "what_foreigners_do_not_know": "Price/quality ratio is exceptional but requires planning",
        "main_hook": "You can get glasses in Korea for 1/3 the US price - but most tourists miss it",
        "controversy_or_curiosity": "curiosity",
        "post_type": "curiosity",
        "comment_1_answer": "Production takes 1-3 hours minimum. Tourists who don't plan miss the time window. Some shops require prescriptions.",
        "comment_2_real_tip": "Best time: morning of mid-trip day. Areas: Namdaemun (cheapest), Hongdae (trendy), Gangnam (premium). Bring current glasses or prescription.",
        "comment_3_pglemaps_benefit": "Save optical shops with surrounding places to see if buying glasses actually fits your route",
        "comment_keyword": "GLASSES",
        "source_needed": "A",  # A급 (가격 자료 필요)
        "current_or_future_feature": "current",
        "forbidden_claims": [
            "Pglemaps recommends specific optical shops",  # 입점 전이므로
            "Compare prices and services",  # 입점 후 기능
            "Direct booking",
        ],
    },
    
    "CLINIC": {
        "category_id": "clinic",
        "category_name": "Korea Beauty Clinic Planning",
        "target_traveler": "K-beauty tourists with clinic appointments",
        "what_foreigners_already_know": "Korea = K-beauty paradise",
        "what_foreigners_do_not_know": "Clinic appointments separated from itinerary cause chaos",
        "main_hook": "Booking K-beauty clinics without planning your day = recipe for chaos",
        "controversy_or_curiosity": "curiosity",
        "post_type": "mistake_warning",
        "comment_1_answer": "Treatments take longer than expected. Recovery time affects rest of day. Wrong location = wasted hours between appointments.",
        "comment_2_real_tip": "Group clinic + nearby cafe + light shopping. Allow recovery buffer. Avoid clinics in areas you don't need otherwise.",
        "comment_3_pglemaps_benefit": "Save beauty spots with nearby places to check if clinic, shopping, cafe stops fit one day",
        "comment_keyword": "CLINIC",
        "source_needed": "B",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Pglemaps recommends specific clinics", "Real-time appointment booking"],
    },
    
    "HAIR": {
        "category_id": "hair",
        "category_name": "Korea Hair Salon Visit",
        "target_traveler": "foreigners curious about Korean hair salons",
        "what_foreigners_already_know": "Korean hair styling = trendy",
        "what_foreigners_do_not_know": "Where you book affects price more than expected",
        "main_hook": "Tourist-area Korean hair salons can cost 3x the local price",
        "controversy_or_curiosity": "controversy",
        "post_type": "controversial",
        "comment_1_answer": "Salons in Myeongdong/Hongdae often inflate foreigner prices. Same service in less touristy areas can be much cheaper.",
        "comment_2_real_tip": "Try less obvious areas: Hapjeong, Yeonnam, Mapo, or Korean-recommended chains. Always confirm price before sitting in chair.",
        "comment_3_pglemaps_benefit": "Save hair salons with surrounding places to plan a realistic day",
        "comment_keyword": "HAIR",
        "source_needed": "B",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Pglemaps recommends specific salons", "Pre-booking through Pglemaps"],
    },
    
    "HANBOK": {
        "category_id": "hanbok",
        "category_name": "Hanbok Rental Decision",
        "target_traveler": "first-time visitors planning palace visits",
        "what_foreigners_already_know": "Wear Hanbok at Gyeongbokgung for photos",
        "what_foreigners_do_not_know": "Where you rent affects the rest of your day",
        "main_hook": "Don't pick a Hanbok rental just because it's close to the palace",
        "controversy_or_curiosity": "curiosity",
        "post_type": "mistake_warning",
        "comment_1_answer": "Rental shops near Gyeongbokgung are crowded, pricier, and tourist-trap-y. Bukchon shops often better quality, less crowded.",
        "comment_2_real_tip": "Plan: rent in Bukchon → walk to Gyeongbokgung → photos → Bukchon village → Ikseon-dong dinner. Free palace entry with Hanbok.",
        "comment_3_pglemaps_benefit": "Save Hanbok shops with palaces, photo spots, restaurants to check the full day",
        "comment_keyword": "HANBOK",
        "source_needed": "C",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Pglemaps recommends specific Hanbok rentals", "Pre-booking discounts"],
    },
    
    "TAXI": {
        "category_id": "taxi",
        "category_name": "Korea Taxi Reality",
        "target_traveler": "first-time Korea travelers assuming taxi is universal",
        "what_foreigners_already_know": "Take taxi when subway is too far",
        "what_foreigners_do_not_know": "Knowing when NOT to taxi matters more",
        "main_hook": "Taxi in Korea isn't your default - here's when it actually saves time",
        "controversy_or_curiosity": "curiosity",
        "post_type": "mistake_warning",
        "comment_1_answer": "Taxi between scattered neighborhoods = expensive and slow during traffic. Subway often faster + cheaper.",
        "comment_2_real_tip": "Use taxi for: late night, hotel/airport, heavy luggage, 1km within neighborhood. Avoid: cross-city trips during 5-8pm.",
        "comment_3_pglemaps_benefit": "Plan routes that don't depend only on taxi between scattered places",
        "comment_keyword": "TAXI",
        "source_needed": "B",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Built-in taxi calling", "Real-time fare estimates"],
    },
    
    "AIRPORT": {
        "category_id": "airport",
        "category_name": "Incheon Airport Transfer",
        "target_traveler": "arriving travelers without transport plan",
        "what_foreigners_already_know": "Airport taxi or train to Seoul",
        "what_foreigners_do_not_know": "Choice depends on hotel area + arrival time + luggage",
        "main_hook": "Taking airport taxi by default is how you start your Korea trip wrong",
        "controversy_or_curiosity": "controversy",
        "post_type": "info",
        "comment_1_answer": "Taxi 60,000-100,000 KRW takes 60-90min. AREX 9,000 KRW takes 45min express. Bus 17,000 KRW depends on hotel.",
        "comment_2_real_tip": "AREX for: Hongdae/Seoul Station area, light luggage. Bus for: direct hotel access. Taxi for: late arrival, heavy luggage, group.",
        "comment_3_pglemaps_benefit": "Save your hotel and major destinations to see which transfer option actually fits",
        "comment_keyword": "AIRPORT",
        "source_needed": "A",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Pglemaps books airport transfer", "Real-time AREX schedule"],
    },
    
    "FOOD": {
        "category_id": "food",
        "category_name": "Korean Restaurant Route",
        "target_traveler": "foodies who saved tons of restaurants",
        "what_foreigners_already_know": "Save TikTok/Instagram restaurants",
        "what_foreigners_do_not_know": "30 saved restaurants don't help if scattered",
        "main_hook": "Saving 30 Korean restaurants doesn't mean you'll actually eat at them",
        "controversy_or_curiosity": "curiosity",
        "post_type": "mistake_warning",
        "comment_1_answer": "Korean dining culture = breakfast/lunch/dinner have different best areas. Scattered restaurants = missing meal times.",
        "comment_2_real_tip": "Group by area + meal time: morning markets in Tongin, lunch in Myeongdong area, dinner in Hongdae/Seongsu. Don't backtrack.",
        "comment_3_pglemaps_benefit": "Save restaurants with cafes, tourist spots to plan realistic meal flow",
        "comment_keyword": "FOOD",
        "source_needed": "C",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Restaurant reservations", "Real-time wait times"],
    },
    
    "SHOPPING": {
        "category_id": "shopping",
        "category_name": "Seoul Shopping Route",
        "target_traveler": "shopaholics planning Seoul shopping",
        "what_foreigners_already_know": "Shop at Myeongdong, Dongdaemun, Gangnam",
        "what_foreigners_do_not_know": "Hotel location + luggage capacity determines best shopping route",
        "main_hook": "Your Seoul shopping plan probably ignores the biggest problem: luggage",
        "controversy_or_curiosity": "curiosity",
        "post_type": "controversial",
        "comment_1_answer": "Big shopping in early trip = carrying bags all day. Last-day shopping = no time for backup. Wrong neighborhood = wasted transfers.",
        "comment_2_real_tip": "Day 1-2: light shopping near hotel. Mid-trip: focused shopping by category. Last day: only small items. Hotel storage helps.",
        "comment_3_pglemaps_benefit": "Save shopping streets with hotel and tourist spots to plan luggage-smart route",
        "comment_keyword": "SHOPPING",
        "source_needed": "B",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Shopping discounts", "Pre-purchase tax refund"],
    },
    
    "RAIN": {
        "category_id": "rain",
        "category_name": "Rainy Day Seoul Plan",
        "target_traveler": "travelers worried about weather",
        "what_foreigners_already_know": "Korea has rainy season in summer",
        "what_foreigners_do_not_know": "Smart travelers prepare backup routes, not just umbrellas",
        "main_hook": "Rainy day in Seoul kills 80% of typical itineraries",
        "controversy_or_curiosity": "controversy",
        "post_type": "curiosity",
        "comment_1_answer": "Outdoor palaces, markets, photo spots ruined by rain. Tourists end up stuck in hotel cafe or shopping mall all day.",
        "comment_2_real_tip": "Indoor backup spots: COEX, Lotte World Mall, Starfield, National Museum, K-pop stores, themed cafes. Plan one near each hotel area.",
        "comment_3_pglemaps_benefit": "Save indoor spots near your hotel to switch plans when weather changes",
        "comment_keyword": "RAIN",
        "source_needed": "C",
        "current_or_future_feature": "current",
        "forbidden_claims": ["Weather forecast integration", "Real-time crowd levels"],
    },
    
    "KOREA": {
        "category_id": "korea",
        "category_name": "First-Time Korea Travel",
        "target_traveler": "first-time visitors over-planning or under-planning",
        "what_foreigners_already_know": "Korea = Seoul, food, K-pop, palaces",
        "what_foreigners_do_not_know": "70% planned + 30% flexible is the magic ratio",
        "main_hook": "Your first Korea trip plan is probably broken in one specific way",
        "controversy_or_curiosity": "curiosity",
        "post_type": "curiosity",
        "comment_1_answer": "Over-planners exhaust themselves. Under-planners waste days deciding. The fix: anchor must-visit places, leave room for discoveries.",
        "comment_2_real_tip": "Plan: 1-2 must-do per day, 1 spontaneous slot, evenings flexible. Lock big things (clinics, shows), let small things flow.",
        "comment_3_pglemaps_benefit": "Organize must-visit places on one map, leave room for spontaneous additions",
        "comment_keyword": "KOREA",
        "source_needed": "C",
        "current_or_future_feature": "current",
        "forbidden_claims": ["AI itinerary generator", "Trip optimization algorithm"],
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
