import asyncio # 로그인 실패 등 브라우저 얼럿 팝업 백그라운드에서 처리하기 위함
from playwright.async_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        
        '''로그인 화면 로케이터 정의'''
        #로그인 입력창
        self.input_userid = page.locator('아이디 입력란 로케이터') 
        self.input_password = page.locator('비밀번호 입력란 로케이터')
        self.btn_login = page.locator('로그인 확인 버튼 로케이터')
        self.auto_login = page.locator('자동로그인 버튼 로케이터')
        
        #간편로그인
        self.login_with_kakao = page.locator('카카오로그인 로케이터')
        self.login_with_apple = page.locator('애플로그인 로케이터')
        self.login_with_email = page.locator('이메일로 로그인 로케이터')

        self.search_id = page.locator('#아이디 찾기 로케이터') 
        self.search_pw = page.locator('비밀번호 찾기 로케이터')

    async def open(self):
        await self.page.goto("로그인 화면 링크") 

    # 이메일 계정 > 정상 로그인 확인 테스트
    async def login_with_valid(self, userid, password):
        await self.input_userid.fill(userid)
        await self.input_password.fill(password)
    
        await self.btn_login.click()

    # 이메일 계정 > 비정상 로그인 확인 테스트
    async def login_with_invalid(self, userid, password): 
        # 첫 번째 : 아이디 미입력시 오류 확인 문자 확인
        async def handle_alert1(dialog):
            assert dialog.message == '아이디를 입력해 주세요.'
            await dialog.accept() #팝업 창 닫기
        
        self.page.once("dialog", lambda dialog: asyncio.create_task(handle_alert1(dialog))) #딱한번 발생 설정
        await self.btn_login.click()
        await self.input_userid.fill(userid)

        # 두 번째: 아이디 입력 후 비밀번호 미입력 시 오류 문자 확인
        async def handle_alert2(dialog):
            assert dialog.message == '비밀번호를 입력해 주세요.'
            await dialog.accept()

        self.page.once("dialog", lambda dialog: asyncio.create_task(handle_alert2(dialog)))
        await self.btn_login.click()
        await self.input_password.fill(password)


        # 세 번째 : 잘못된 계정(로그인/비밀번호 모두 입력) 로그인 실패 오류 문자 확인
        async def handle_alert3(dialog):
            assert dialog.message == '아이디 또는 패스워드를 확인하세요.'
            await dialog.accept()

        self.page.once("dialog", lambda dialog: asyncio.create_task(handle_alert3(dialog)))
        await self.btn_login.click()


    # 자동로그인, 카카오 로그인, Apple로 로그인, 회원가입 
    async def login_etc(self):
        # 자동로그인 확인 케이스
        async def handle_auto_login_alert(dialog):
            assert dialog.message == '본인 기기에서만 이용해주세요.' # 선택 시 알람 문구
            await dialog.accept() #문구 맞으면 닫아 그냥 토스트일경우 삭제
            
        self.page.once("dialog", lambda dialog: asyncio.create_task(handle_auto_login_alert(dialog)))
        await self.auto_login.click() #팝업 아니면 삭제하기
        
        auto_elem = self.page.locator('#tooltipAutoLogin')
        await expect(auto_elem).to_have_class('ui-toggle-btn is-active') 
        await self.auto_login.click()
        await expect(auto_elem).to_have_class('ui-toggle-btn') # 체크표시 삭제되어 있는지

        # 카카오 로그인
        await self.login_with_kakao.click()
        await self.page.go_back()
        await self.page.wait_for_timeout(2000)

        # Apple로 로그인
        await self.login_with_apple.click()
        await self.page.go_back()
        await self.page.wait_for_timeout(2000)

    # 아이디 찾기
    async def search_member_id(self):
        await self.search_id.click()
   
    # 비밀번호 찾기
    async def search_member_pw(self):
        await self.search_pw.click()
