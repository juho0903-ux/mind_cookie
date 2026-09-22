"""마음쿠키: AI/API 호출 없는 감정별 문구 앱. streamlit run app.py"""
import html
import random
import time
import streamlit as st

st.set_page_config(page_title="오늘의 마음쿠키", page_icon="🥠", layout="wide")
GROUPS = {}
GROUPS['☀️ 기분 좋은 마음'] = ['가벼운', '상쾌한', '포근한', '가슴뭉클한', '생기가 도는', '푸근한', '감격스러운', '설레는', '행복한', '감사한', '신나는', '환희에 찬', '개운한', '싱그러운', '홀가분한', '경이로운', '안심이 되는', '황홀한', '고마운', '여유로운', '후련한', '기대되는', '영광스러운', '흐뭇한', '기쁜', '용기 나는', '흥미로운', '기운이 나는', '유쾌한', '희망을 느끼는', '끌리는', '재미있는', '활기 넘치는', '다정한', '자랑스러운', '달콤한', '정겨운', '든든한', '정다운', '따뜻한', '즐거운', '떳떳한', '짜릿한', '마음이 놓이는', '친근한', '만족스러운', '쾌활한', '명랑한', '통쾌한', '반가운', '편안한', '뿌듯한', '평화로운', '산뜻한']
GROUPS['🌧️ 마음이 힘든 순간'] = ['갑갑한', '민망한', '어색한', '겁나는', '비참한', '열받은', '걱정스러운', '불편한', '오싹한', '격분한', '불안한', '외로운', '곤혹스러운', '분한', '우울한', '공허한', '부끄러운', '울적한', '괴로운', '서글픈', '지루한', '귀찮은', '서먹한', '지친', '근심스러운', '서운한', '참담한', '꺼림칙한', '섭섭한', '창피한', '낙담한', '성가신', '초조한', '난감한', '속상한', '피곤한', '난처한', '속타는', '화나는', '답답한', '슬픈', '당혹스런', '신경쓰이는', '두려운', '실망한', '따분한', '심심한', '막막한', '쓸쓸한', '멋쩍은', '아쉬운', '무기력한', '안타까운', '무서운', '암담한', '무안한', '억울한']
GROUPS['🌈 여러 빛깔의 마음'] = ['긴장이 풀리는', '느긋한', '든든해지는', '궁금한', '긴장되는', '놀란', '떨리는', '멍한', '묘한', '벅찬', '어리둥절한', '얼떨떨한', '흥분되는']

st.markdown('''<style>
.stApp{background:#faf9f2;color:#344337} .block-container{max-width:1120px;padding-top:2rem} h1,h2,h3{color:#365b40!important;letter-spacing:-.04em} [data-testid="stSidebar"]{background:#f0f3e8} [data-testid="stButton"] button{border-radius:14px;border-color:#d8e1cf;min-height:44px} [data-testid="stButton"] button[kind="primary"]{background:#46734e;border-color:#46734e;color:white} [data-testid="stTextArea"] textarea,[data-testid="stTextInput"] input{background:#fffef9;border-radius:12px} .top{display:flex;justify-content:space-between;border-bottom:1px solid #dce2d1;padding-bottom:18px;color:#66785b}.brand{font-size:22px;font-weight:800}.sub{font-size:13px}.kicker{font-size:13px;letter-spacing:3px;color:#83926c;margin-top:25px}.headline{font-size:42px;font-weight:800;line-height:1.35;margin:12px 0;color:#345c40}.intro{color:#7a8370;margin-bottom:28px}.cookie-box{border-radius:24px;background:#edf1dc;padding:25px;text-align:center;margin-bottom:20px;border:1px solid #dce3c7}.cookie{font-size:100px;line-height:1.5;display:inline-block;transform:rotate(-12deg)}.cookie-title{font-size:22px;font-weight:700;color:#486343}.cookie-sub{font-size:14px;color:#7b866c;line-height:1.8}.paper{background:#fffef8;border-radius:12px;border:1px solid #e3e6d7;padding:28px;margin:15px 0;box-shadow:0 6px 0 #e9eddf;animation:slide .6s ease}.paper .message{font-size:18px;line-height:1.95;word-break:keep-all}.paper .bonus{border-top:1px dashed #ccd5be;padding-top:18px;font-size:15px;line-height:1.8}.selected{display:inline-block;background:#e5efd9;color:#45643a;border-radius:20px;padding:7px 15px;margin:4px}.footer{font-size:12px;color:#8a927f;text-align:center;padding-top:28px}.shake{animation:shake .4s infinite}@keyframes shake{50%{transform:rotate(14deg)}}@keyframes slide{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}@media(max-width:600px){.headline{font-size:32px}.sub{display:none}.block-container{padding:1rem}.paper{padding:20px}}@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>''', unsafe_allow_html=True)
# 고정 문구를 감정 계열에 따라 선택합니다. AI 추론이나 사연 분석은 하지 않습니다.
FAMILIES = {
    'anger': '격분한 분한 열받은 화나는 억울한'.split(),
    'worry': '겁나는 걱정스러운 불안한 근심스러운 초조한 속타는 두려운 막막한 무서운 꺼림칙한 오싹한 신경쓰이는 긴장되는 떨리는'.split(),
    'sad': '비참한 외로운 우울한 공허한 울적한 괴로운 서글픈 서운한 참담한 섭섭한 낙담한 속상한 슬픈 실망한 쓸쓸한 아쉬운 안타까운 암담한'.split(),
    'tired': '귀찮은 지친 피곤한 무기력한 성가신 지루한 따분한 심심한 갑갑한 답답한'.split(),
    'awkward': '민망한 어색한 불편한 곤혹스러운 부끄러운 서먹한 창피한 난감한 난처한 당혹스런 멋쩍은 무안한 어리둥절한 얼떨떨한'.split(),
    'proud': '감격스러운 영광스러운 흐뭇한 자랑스러운 떳떳한 만족스러운 뿌듯한'.split(),
    'calm': ['가벼운','포근한','푸근한','개운한','홀가분한','안심이 되는','여유로운','후련한','든든한','마음이 놓이는','편안한','평화로운','긴장이 풀리는','느긋한','든든해지는'],
    'warm': '감사한 고마운 다정한 정겨운 정다운 따뜻한 친근한 반가운'.split(),
    'excited': ['설레는','기대되는','흥미로운','끌리는','궁금한','흥분되는','희망을 느끼는'],
}
BANK = {
'anger': [
('화가 나는 마음도 알아차려 줄 필요가 있어. 그 마음을 느끼는 것과 곧바로 행동하는 것은 따로 선택할 수 있어. 잠깐 멈추고 하고 싶은 말을 먼저 적어 봐도 좋아.','오늘의 작은 한 걸음','지금 원하는 것을 한 문장으로 적어 보기.'),
('억지로 괜찮은 척하지 않아도 돼. 마음이 뜨거울 때는 대답을 조금 늦춰도 괜찮아. 잠시 쉴 수 있는 곳을 찾아볼까?','마음 질문','내가 바라는 변화는 무엇일까?')],
'worry': [
('걱정이나 긴장 때문에 마음이 바쁠 수 있어. 지금 모든 답을 찾아야 하는 건 아니야. 오늘 확인할 수 있는 것 하나부터 골라 봐도 좋아.','오늘의 작은 한 걸음','지금 아는 사실과 아직 모르는 것을 하나씩 적기.'),
('마음이 조마조마한 날도 있어. 불확실한 일이 있다고 해서 혼자 다 해결해야 하는 것은 아니야. 도움이 필요한 부분을 한 가지 골라 볼까?','마음 질문','누구에게 어떤 도움을 부탁하고 싶을까?')],
'sad': [
('마음이 가라앉거나 아픈 순간에는 쉽게 말이 나오지 않을 수 있어. 바로 괜찮아져야 할 필요는 없어. 편하게 이야기할 수 있는 사람을 떠올려 봐도 좋아.','오늘의 작은 한 걸음','내 이야기를 들어줬으면 하는 사람 한 명 떠올리기.'),
('지금의 마음을 작게 여기지 않아도 돼. 다른 사람과 비교해서 얼마나 속상한지 증명할 필요는 없어. 오늘 나에게 조금 편안한 시간을 줘 볼까?','마음 질문','지금 듣고 싶은 말은 무엇일까?')],
'tired': [
('몸이나 마음이 쉬고 싶은 날도 있어. 오늘의 기운이 네 가치나 실력을 정하지는 않아. 잠시 쉬었다가 할 수 있는 만큼만 해 봐도 좋아.','오늘의 작은 한 걸음','어깨에 힘을 풀고 잠깐 쉬기.'),
('의욕이 잘 나지 않는 순간도 있지. 지금 당장 큰 일을 시작할 필요는 없어. 쉬기와 작은 일 하나 중 지금 필요한 것을 골라 봐.','마음 질문','지금 필요한 건 쉼일까, 작은 변화일까?')],
'awkward': [
('어색하거나 당황스러운 마음이 들 때도 있어. 한 순간의 느낌으로 너 전체를 평가하지 않아도 돼. 마음을 정리할 시간을 조금 가져도 괜찮아.','오늘의 작은 한 걸음','지금 마음을 설명하는 짧은 문장 하나 적기.'),
('말이나 표정이 마음처럼 되지 않는 날도 있어. 모든 순간에 완벽하게 반응할 필요는 없어. 다음에 하고 싶은 말을 천천히 생각해 봐도 좋아.','마음 질문','다시 말할 기회가 있다면 무엇을 전하고 싶을까?')],
'proud': [
('스스로 뿌듯하게 느껴지는 마음을 충분히 누려도 좋아. 결과뿐 아니라 네가 했던 선택과 노력도 기억할 만해. 오늘의 나에게 칭찬 하나 남겨 볼까?','오늘의 작은 한 걸음','내가 잘한 행동 한 가지 적기.'),
('자신에게 고개를 끄덕여 주고 싶은 날이네. 다른 사람의 인정이 없어도 네가 느낀 만족에는 의미가 있어. 기억하고 싶은 순간을 하나 골라 봐.','마음 질문','이번에 내가 스스로 인정해 주고 싶은 점은?')],
'calm': [
('조금 편안해진 마음을 그대로 누려도 좋아. 쉬는 순간까지 알차게 채울 필요는 없어. 지금 편안한 감각 하나를 찾아볼까?','오늘의 작은 한 걸음','주변에서 보기 편안한 것을 하나 찾아보기.'),
('마음에 여유가 느껴지는 순간이구나. 특별한 일이 없어도 이런 시간은 소중해. 잠깐 아무것도 서두르지 않아도 괜찮아.','마음 질문','지금의 편안함을 도와준 것은 무엇일까?')],
'warm': [
('따뜻하게 느껴지는 마음을 만났구나. 그 마음은 꼭 거창한 말로 표현하지 않아도 돼. 떠오르는 사람이나 순간을 조용히 기억해 봐도 좋아.','오늘의 작은 한 걸음','고마웠던 순간을 한 줄로 적어 보기.'),
('다정한 마음이 드는 순간을 조금 더 느껴 봐도 좋아. 표현할지 말지는 네가 골라도 괜찮아. 전하고 싶다면 짧은 말 한마디로도 충분해.','마음 질문','이 마음을 어떤 방식으로 남기고 싶을까?')],
'excited': [
('무언가를 기대하는 마음이 있구나. 결과를 미리 정하지 않아도 지금의 관심을 즐길 수 있어. 궁금한 것 하나를 살펴봐도 좋아.','오늘의 작은 한 걸음','기대되는 점을 하나 적어 보기.'),
('마음이 향하는 것이 있는 날이네. 좋아하는 것을 알아가는 일에도 네 속도가 있어. 오늘 해 보고 싶은 작은 시도 하나를 골라 봐.','마음 질문','어떤 점이 나를 가장 궁금하게 만들까?')],
'joy': [
('기분 좋은 마음을 충분히 느껴도 좋아. 특별한 이유를 설명해야만 즐거워할 수 있는 건 아니야. 지금의 순간에서 기억하고 싶은 것을 하나 골라 볼까?','오늘의 작은 한 걸음','오늘 좋았던 순간을 세 단어로 남기기.'),
('밝아진 마음을 만난 순간이구나. 기쁨의 크기를 다른 사람과 비교하지 않아도 돼. 너만의 방식으로 이 순간을 누려 봐.','마음 질문','오늘 다시 떠올리고 싶은 순간은?')],
'mixed': [
('지금의 마음이 한마디로 딱 정리되지 않을 수도 있어. 바로 뜻을 알아내야 하는 것은 아니야. 조금 더 머물며 마음을 살펴봐도 좋아.','마음 질문','이 마음과 함께 떠오르는 다른 단어는?'),
('낯설거나 묘한 느낌이 찾아올 때도 있어. 마음에 정확한 이름을 붙이지 못해도 괜찮아. 지금 몸과 마음이 어떤지 천천히 살펴볼까?','오늘의 작은 한 걸음','눈에 보이는 것과 들리는 소리를 하나씩 찾아보기.')],
}

def family(word):
    for name, words in FAMILIES.items():
        if word in words:
            return name
    return 'joy' if word in GROUPS['☀️ 기분 좋은 마음'] else 'mixed'

def make_cookie(words, previous=None):
    families = list(dict.fromkeys(family(w) for w in words))
    candidates = [item for f in families for item in BANK[f]]
    choices = [c for c in candidates if not previous or c[0] != previous['base']]
    base, title, action = random.choice(choices or candidates)
    if len(families) > 1:
        message = f'‘{words[0]}’ 마음과 ‘{words[1]}’ 마음이 함께 있구나. 둘 중 하나를 지우거나 어느 쪽이 진짜인지 정하지 않아도 돼. 지금 조금 더 돌보고 싶은 마음부터 살펴봐도 좋아.'
        # 조합의 두 감정을 인정하고, 고른 감정 계열의 질문/행동을 제시합니다.
    else:
        message = base
    return {'message': message, 'title': title, 'action': action, 'base': base, 'words': tuple(words)}

for key, value in {'selected': [], 'result': None, 'search': ''}.items():
    if key not in st.session_state:
        st.session_state[key] = value

def choose(word):
    selected = st.session_state.selected
    if word in selected:
        selected.remove(word)
    elif len(selected) < 2:
        selected.append(word)
    else:
        st.toast('마음 단어는 두 개까지 고를 수 있어요. 🥠')
    st.session_state.result = None

def reset():
    st.session_state.selected = []
    st.session_state.result = None
    st.session_state.search = ''

st.markdown('<div class="top"><span class="brand">🥠 마음쿠키</span><span class="sub">잠깐, 내 마음을 만나는 시간</span></div><div class="kicker">오늘의 마음 한 조각</div><div class="headline">오늘 너의 마음은 어떤 맛이야?</div><div class="intro">마음과 닮은 단어를 고르고, 작은 한마디를 만나 보세요.</div>', unsafe_allow_html=True)
st.caption('AI가 답하는 서비스가 아니에요. 선택한 감정에 맞춰 미리 준비한 문구를 보여줘요.')
left, right = st.columns([1.5, 1], gap='large')
with left:
    st.subheader('마음에 이름 붙이기')
    st.caption('두 개까지 골라 보세요. 하나만 골라도 괜찮아요.')
    query = st.text_input('감정 단어 찾기', placeholder='내 마음과 비슷한 단어 찾기 🔍', key='search').strip()
    def buttons(words):
        with st.container(height=320, border=False):
            columns = st.columns(3)
            for i, word in enumerate(words):
                chosen = word in st.session_state.selected
                columns[i % 3].button(('✓ ' if chosen else '') + word, key='word_' + word, type='primary' if chosen else 'secondary', use_container_width=True, on_click=choose, args=(word,))
    if query:
        matches = [w for words in GROUPS.values() for w in words if query in w]
        if matches:
            buttons(matches)
        else:
            st.info('닮은 단어가 없어요. 다른 말로 찾아볼까요?')
    else:
        for tab, words in zip(st.tabs(list(GROUPS)), GROUPS.values()):
            with tab:
                buttons(words)
    st.caption(f'{len(st.session_state.selected)} / 2 선택했어요')
    st.markdown(''.join('<span class="selected">' + html.escape(w) + '</span>' for w in st.session_state.selected), unsafe_allow_html=True)
with right:
    st.markdown('<div class="cookie-box"><div class="kicker">A LITTLE NOTE FOR YOU</div><span class="cookie">🥠</span><div class="cookie-title">마음을 살피는 작은 한마디</div><p class="cookie-sub">달콤한 날도, 조금 쌉싸름한 날도.<br>여기서는 있는 그대로 괜찮아요.</p></div>', unsafe_allow_html=True)
    if st.button('🥠 다른 마음쿠키 열기' if st.session_state.result else '🥠 내 마음쿠키 열기', type='primary', use_container_width=True, disabled=not st.session_state.selected):
        with st.spinner('쿠키를 열고 있어요…'):
            time.sleep(.6)
            st.session_state.result = make_cookie(st.session_state.selected, st.session_state.result)
    result = st.session_state.result
    if result:
        st.markdown('<div class="paper"><div class="kicker">오늘 너의 마음은</div><h3>' + html.escape(' + '.join(result['words'])) + '</h3><p class="message">' + html.escape(result['message']) + '</p><div class="bonus"><strong>✦ ' + html.escape(result['title']) + '</strong><br>' + html.escape(result['action']) + '</div></div>', unsafe_allow_html=True)
        st.caption('이 문구가 내 마음과 다르면, 다른 쿠키를 열거나 감정을 다시 골라도 괜찮아요.')
        st.button('↩ 오늘 마음 다시 고르기', on_click=reset, use_container_width=True)
    st.caption('마음이 많이 힘들거나 안전하지 않다면, 믿을 수 있는 선생님이나 보호자에게 알려 주세요.')
st.markdown('<div class="footer">사연·이름·연락처를 입력받지 않아요. 외부 AI에 전송하지 않아요.<br>선택한 감정은 현재 세션에서만 사용하며, 앱은 파일이나 데이터베이스에 저장하지 않아요.</div>', unsafe_allow_html=True)
