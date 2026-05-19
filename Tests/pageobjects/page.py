from playwright.async_api import Page

#모든 페이지 오브젝트에서 공통으로 공유하는 메서드,기능을 담고 있는 메인 부모 클래스
class BasePage:

    def __init__(self, page: Page):
        # 브라우저 페이지 객체를 받아와서 클래스 내부에 저장
        self.page = page

    async def open(self, path: str = ""):
        # 로그인 페이지 여는 메서드
        
        return await self.page.goto("여기 이메일")