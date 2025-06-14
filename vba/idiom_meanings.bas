Function GetIdiomMeaning(ByVal idiom As String) As String
    Dim dict As Object
    Set dict = CreateObject("Scripting.Dictionary")

    ' Add idioms and their meanings here
    dict.Add "일석이조", "한 가지 일을 하여 두 가지 이익을 얻음"
    dict.Add "사필귀정", "모든 일은 결국 올바른 이치로 돌아감"
    dict.Add "백문불여일견", "백 번 듣는 것이 한 번 보는 것만 못함"
    dict.Add "고진감래", "괴로움이 지나가면 즐거움이 옴"
    dict.Add "동문서답", "묻는 말에 대하여 딴소리를 함"

    If dict.Exists(idiom) Then
        GetIdiomMeaning = dict(idiom)
    Else
        GetIdiomMeaning = "사전에서 찾을 수 없습니다"
    End If
End Function
