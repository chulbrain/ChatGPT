# ChatGPT

## VBA function for 사자성어 lookup

`vba/idiom_meanings.bas` 파일에는 간단한 사자성어 사전이 들어 있는 VBA 함수 `GetIdiomMeaning`이 포함되어 있습니다. Excel에서 다음과 같이 사용할 수 있습니다.

1. Excel에서 VBA 편집기를 열고(Module을 추가합니다).
2. `idiom_meanings.bas` 파일의 코드를 복사하여 모듈에 붙여넣습니다.
3. 셀에 사자성어를 입력하고, 다른 셀에서 `=GetIdiomMeaning(A1)` 형식으로 함수를 호출하면 뜻이 표시됩니다.

사전에 없는 사자성어를 입력하면 "사전에서 찾을 수 없습니다"라는 메시지를 반환합니다.
