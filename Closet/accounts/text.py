def message(domain, uidb64, token):
    return f"<가입 인증 메일> \n\n아래 링크를 클릭하여 회원가입 인증을 완료해주세요. \n\n가입 인증 링크 : http://{domain}/accounts/activate/{uidb64}/{token} \n\n from ICE CLOSET"
