  [OK] Non-ASCII = 0
  [OK] Wrong-range ChrW = 0
  [OK] No duplicate names
  [OK] No Then+colon+GoTo
  [OK] bSingle declared
  [OK] bMulti declared
  [OK] Worksheet explicit (>=8)
  [OK] .Text reads (>=8)
  [OK] IsEmpty guards (>=3)
  [OK] vbNullString (>=2)
  [FAIL] ReDim on own line
  [OK] Do While trailing+

Lines: 537  Status: FAIL
ET NAME FUNCTIONS =====
Private Function SH_BLANK() As String: SH_BLANK = ChrW(3615) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3617) & ChrW(3648) & ChrW(3611) & ChrW(3621) & ChrW(3656) & ChrW(3634): End Function
Private Function SH_FORM2() As String: SH_FORM2 = ChrW(3615) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3617) & ChrW(3648) & ChrW(3610) & ChrW(3636) & ChrW(3585) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640): End Function
Private Function SH_DASH2() As String: SH_DASH2 = ChrW(3649) & ChrW(3604) & ChrW(3594) & ChrW(3610) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3604) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640): End Function
Private Function MONTH_PFX() As String: MONTH_PFX = ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609): End Function

' ===== UI STRING FUNCTIONS =====
Private Function T_NO_MONTH() As String: T_NO_MONTH = ChrW(3618) & ChrW(3633) & ChrW(3591) & ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609) & ChrW(32) & ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3626) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3591) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609) & ChrW(3585) & ChrW(3656) & ChrW(3629) & ChrW(3609): End Function
Private Function T_AVAIL_SH() As String: T_AVAIL_SH = ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(3629) & ChrW(3618) & ChrW(3641) & ChrW(3656) & ChrW(58): End Function
Private Function T_TYPE_SH() As String: T_TYPE_SH = ChrW(3614) & ChrW(3636) & ChrW(3617) & ChrW(3614) & ChrW(3660) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609) & ChrW(58): End Function
Private Function T_SH_TTL() As String: T_SH_TTL = ChrW(3648) & ChrW(3621) & ChrW(3639) & ChrW(3629) & ChrW(3585) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609): End Function
Private Function T_SH_NF() As String: T_SH_NF = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3614) & ChrW(3610) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(58): End Function
Private Function T_WORKERS() As String: T_WORKERS = ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3594) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(58): End Function
Private Function T_TYPE_WK() As String: T_TYPE_WK = ChrW(3614) & ChrW(3636) & ChrW(3617) & ChrW(3614) & ChrW(3660) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3594) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(58): End Function
Private Function T_WK_TTL() As String: T_WK_TTL = ChrW(3648) & ChrW(3621) & ChrW(3639) & ChrW(3629) & ChrW(3585) & ChrW(3594) & ChrW(3656) & ChrW(3634) & ChrW(3591): End Function
Private Function T_WK_NF() As String: T_WK_NF = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3614) & ChrW(3610) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3594) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(3651) & ChrW(3609) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(32) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3605) & ChrW(3657) & ChrW(3629) & ChrW(3591) & ChrW(3605) & ChrW(3619) & ChrW(3591) & ChrW(3585) & ChrW(3633) & ChrW(3610) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(3651) & ChrW(3609) & ChrW(3605) & ChrW(3634) & ChrW(3619) & ChrW(3634) & ChrW(3591): End Function
Private Function T_MATS() As String: T_MATS = ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640) & ChrW(58): End Function
Private Function T_TYPE_MAT() As String: T_TYPE_MAT = ChrW(3614) & ChrW(3636) & ChrW(3617) & ChrW(3614) & ChrW(3660) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640) & ChrW(58): End Function
Private Function T_MAT_TTL() As String: T_MAT_TTL = ChrW(3648) & ChrW(3621) & ChrW(3639) & ChrW(3629) & ChrW(3585) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640): End Function
Private Function T_MAT_NF() As String: T_MAT_NF = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3614) & ChrW(3610) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640) & ChrW(58): End Function
Private Function T_CURR_VAL() As String: T_CURR_VAL = ChrW(3588) & ChrW(3656) & ChrW(3634) & ChrW(3611) & ChrW(3633) & ChrW(3592) & ChrW(3592) & ChrW(3640) & ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(58): End Function
Private Function T_TOT_PCS() As String: T_TOT_PCS = ChrW(3619) & ChrW(3623) & ChrW(3617) & ChrW(32) & ChrW(40) & ChrW(3594) & ChrW(3636) & ChrW(3657) & ChrW(3609) & ChrW(41) & ChrW(58): End Function
Private Function T_QTY_P() As String: T_QTY_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3605) & ChrW(3657) & ChrW(3629) & ChrW(3591) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3648) & ChrW(3610) & ChrW(3636) & ChrW(3585) & ChrW(32) & ChrW(40) & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3648) & ChrW(3605) & ChrW(3655) & ChrW(3617) & ChrW(3648) & ChrW(3607) & ChrW(3656) & ChrW(3634) & ChrW(3609) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(41) & ChrW(58): End Function
Private Function T_QTY_T() As String: T_QTY_T = ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3648) & ChrW(3610) & ChrW(3636) & ChrW(3585): End Function
Private Function T_QTY_INT() As String: T_QTY_INT = ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3648) & ChrW(3605) & ChrW(3655) & ChrW(3617) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3617) & ChrW(3634) & ChrW(3585) & ChrW(3585) & ChrW(3623) & ChrW(3656) & ChrW(3634) & ChrW(32) & ChrW(48): End Function
Private Function T_WD_SAVED() As String: T_WD_SAVED = ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3648) & ChrW(3610) & ChrW(3636) & ChrW(3585) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592) & ChrW(33): End Function
Private Function T_WD_SHEET() As String: T_WD_SHEET = ChrW(3594) & ChrW(3637) & ChrW(3605): End Function
Private Function T_WD_WK() As String: T_WD_WK = ChrW(3594) & ChrW(3656) & ChrW(3634) & ChrW(3591): End Function
Private Function T_WD_MAT() As String: T_WD_MAT = ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640): End Function
Private Function T_WD_ADD() As String: T_WD_ADD = ChrW(3648) & ChrW(3610) & ChrW(3636) & ChrW(3585) & ChrW(3648) & ChrW(3614) & ChrW(3636) & ChrW(3656) & ChrW(3617): End Function
Private Function T_WD_OLD() As String: T_WD_OLD = ChrW(3588) & ChrW(3656) & ChrW(3634) & ChrW(3648) & ChrW(3604) & ChrW(3636) & ChrW(3617): End Function
Private Function T_WD_NEW() As String: T_WD_NEW = ChrW(3588) & ChrW(3656) & ChrW(3634) & ChrW(3651) & ChrW(3627) & ChrW(3617) & ChrW(3656): End Function
Private Function T_WD_TOT() As String: T_WD_TOT = ChrW(3619) & ChrW(3623) & ChrW(3617) & ChrW(3626) & ChrW(3632) & ChrW(3626) & ChrW(3617): End Function
Private Function T_PCS() As String: T_PCS = ChrW(3594) & ChrW(3636) & ChrW(3657) & ChrW(3609): End Function
Private Function T_EMPTY_V() As String: T_EMPTY_V = ChrW(40) & ChrW(3623) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(41): End Function
Private Function T_MULTI_P() As String: T_MULTI_P = ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640) & ChrW(32) & ChrW(40) & ChrW(3648) & ChrW(3623) & ChrW(3657) & ChrW(3609) & ChrW(3623) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(3648) & ChrW(3614) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3627) & ChrW(3618) & ChrW(3640) & ChrW(3604) & ChrW(41) & ChrW(58): End Function
Private Function T_MULTI_T() As String: T_MULTI_T = ChrW(3648) & ChrW(3610) & ChrW(3636) & ChrW(3585) & ChrW(3627) & ChrW(3621) & ChrW(3634) & ChrW(3618) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619): End Function
Private Function T_MULTI_OK() As String: T_MULTI_OK = ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592): End Function
Private Function T_NO_SAVE() As String: T_NO_SAVE = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585): End Function
Private Function T_NEW_SH_T() As String: T_NEW_SH_T = ChrW(3626) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3591) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609) & ChrW(3651) & ChrW(3627) & ChrW(3617) & ChrW(3656): End Function
Private Function T_NEW_SH_E() As String: T_NEW_SH_E = ChrW(3605) & ChrW(3633) & ChrW(3623) & ChrW(3629) & ChrW(3618) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(58): End Function
Private Function T_SH_CNT() As String: T_SH_CNT = ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(3629) & ChrW(3618) & ChrW(3641) & ChrW(3656) & ChrW(58): End Function
Private Function T_SH_EXIST() As String: T_SH_EXIST = ChrW(3617) & ChrW(3637) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3609) & ChrW(3637) & ChrW(3657) & ChrW(3629) & ChrW(3618) & ChrW(3641) & ChrW(3656) & ChrW(3649) & ChrW(3621) & ChrW(3657) & ChrW(3623) & ChrW(58): End Function
Private Function T_TMPL_ERR() As String: T_TMPL_ERR = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3614) & ChrW(3610) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3605) & ChrW(3657) & ChrW(3609) & ChrW(3649) & ChrW(3610) & ChrW(3610) & ChrW(58): End Function
Private Function T_SH_OK() As String: T_SH_OK = ChrW(3626) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3591) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592) & ChrW(58): End Function
Private Function T_SH_COPY() As String: T_SH_COPY = ChrW(3588) & ChrW(3633) & ChrW(3604) & ChrW(3621) & ChrW(3629) & ChrW(3585) & ChrW(3592) & ChrW(3634) & ChrW(3585) & ChrW(3605) & ChrW(3657) & ChrW(3609) & ChrW(3649) & ChrW(3610) & ChrW(3610) & ChrW(3649) & ChrW(3621) & ChrW(3632) & ChrW(3621) & ChrW(3657) & ChrW(3634) & ChrW(3591) & ChrW(3586) & ChrW(3657) & ChrW(3629) & ChrW(3617) & ChrW(3641) & ChrW(3621) & ChrW(3649) & ChrW(3621) & ChrW(3657) & ChrW(3623): End Function
Private Function T_DASH_OK() As String: T_DASH_OK = ChrW(3619) & ChrW(3637) & ChrW(3648) & ChrW(3615) & ChrW(3619) & ChrW(3594) & ChrW(3649) & ChrW(3604) & ChrW(3594) & ChrW(3610) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3604) & ChrW(3623) & ChrW(3633) & ChrW(3626) & ChrW(3604) & ChrW(3640) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592): End Function
Private Function T_NO_MNTH() As String: T_NO_MNTH = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3614) & ChrW(3610) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609): End Function
Private Function T_DONE() As String: T_DONE = ChrW(3648) & ChrW(3626) & ChrW(3619) & ChrW(3655) & ChrW(3592) & ChrW(3626) & ChrW(3636) & ChrW(3657) & ChrW(3609): End Function
Private Function T_ERR() As String: T_ERR = ChrW(3648) & ChrW(3585) & ChrW(3636) & ChrW(3604) & ChrW(3586) & ChrW(3657) & ChrW(3629) & ChrW(3612) & ChrW(3636) & ChrW(3604) & ChrW(3614) & ChrW(3621) & ChrW(3634) & ChrW(3604) & ChrW(58): End Function
Private Function T_SAVED_N() As String: T_SAVED_N = ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(58): End Function

' ===== MODULE-LEVEL CONSTANTS =====
Const ROW_MAT_HDR   As Integer = 1
Const COL_WORKER    As Integer = 1
Const MAT_COL_START As Integer = 2

' ===== ENTRY POINTS =====
Sub ShowWithdrawForm()
    Dim bSingle As Boolean
    bSingle = False
    Call WithdrawWizard(bSingle)
End Sub

Sub ShowMultiWithdrawForm()
    Dim bMulti As Boolean
    bMulti = True
    Call WithdrawWizard(bMulti)
End Sub

Sub CreateNewMonthSheet(): Call NewMonthWizard: End Sub
Sub RefreshDashboard2(): Call BuildDashboard2: End Sub

' ===== SheetExists =====
Function SheetExists(sNm As String) As Boolean
    Dim wTmp As Worksheet
    On Error Resume Next
    Set wTmp = ThisWorkbook.Worksheets(sNm)
    On Error GoTo 0
    SheetExists = Not (wTmp Is Nothing)
End Function

' ===== WithdrawWizard =====
Private Sub WithdrawWizard(bMultiMode As Boolean)
    On Error GoTo ErrWW
    Dim shArr As Variant
    shArr = GetMonthSheets()
    If IsEmpty(shArr) Then
        MsgBox T_NO_MONTH(), vbExclamation
        Exit Sub
    End If
    Dim shLst As String
    shLst = T_AVAIL_SH() & Chr(13) & Chr(13)
    Dim ix As Integer
    For ix = 0 To UBound(shArr)
        shLst = shLst & (ix + 1) & ")  " & CStr(shArr(ix)) & Chr(13)
    Next ix
    Dim shIn As String
    shIn = InputBox(shLst & Chr(13) & T_TYPE_SH(), T_SH_TTL(), CStr(shArr(UBound(shArr))))
    If shIn = "" Then Exit Sub
    If Not SheetExists(shIn) Then
        MsgBox T_SH_NF() & " " & shIn, vbExclamation
        Exit Sub
    End If
    Dim wkArr As Variant
    wkArr = GetWorkers(shIn)
    If IsEmpty(wkArr) Then
        MsgBox T_WK_NF(), vbExclamation
        Exit Sub
    End If
    Dim wkLst As String
    wkLst = T_WORKERS() & Chr(13) & Chr(13)
    For ix = 0 To UBound(wkArr)
        wkLst = wkLst & (ix + 1) & ")  " & CStr(wkArr(ix)) & Chr(13)
    Next ix
    Dim wkIn As String
    wkIn = InputBox(wkLst & Chr(13) & T_TYPE_WK(), T_WK_TTL())
    If Trim(wkIn) = "" Then Exit Sub
    Dim wsSrc As Worksheet
    Set wsSrc = ThisWorkbook.Worksheets(shIn)
    If FindWorkerRow(wsSrc, wkIn) = -1 Then
        MsgBox T_WK_NF(), vbExclamation
        Exit Sub
    End If
    Dim mArr As Variant
    mArr = GetMaterials(shIn)
    If IsEmpty(mArr) Then
        MsgBox T_MAT_NF() & " (empty)", vbExclamation
        Exit Sub
    End If
    Dim mLst As String
    mLst = T_MATS() & Chr(13) & Chr(13)
    For ix = 0 To UBound(mArr)
        mLst = mLst & (ix + 1) & ")  " & CStr(mArr(ix)) & Chr(13)
    Next ix
    If Not bMultiMode Then
        Dim matIn1 As String
        matIn1 = InputBox(mLst & Chr(13) & T_TYPE_MAT(), T_MAT_TTL())
        If matIn1 = "" Then Exit Sub
        Dim mC1 As Long
        mC1 = FindMaterialCol(wsSrc, matIn1)
        If mC1 = -1 Then
            MsgBox T_MAT_NF() & " " & matIn1, vbExclamation
            Exit Sub
        End If
        Dim wR1 As Long
        wR1 = FindWorkerRow(wsSrc, wkIn)
        Dim cur1 As String
        cur1 = Trim(wsSrc.Cells(wR1, mC1).Text)
        Dim num1 As Long
        num1 = ParseNPlus(cur1)
        Dim qStr1 As String
        qStr1 = InputBox(T_CURR_VAL() & " " & IIf(cur1 = "", T_EMPTY_V(), cur1) & _
                         "  " & T_TOT_PCS() & " " & num1 & Chr(13) & Chr(13) & T_QTY_P(), T_QTY_T())
        If qStr1 = "" Then Exit Sub
        If Not IsNumeric(qStr1) Then
            MsgBox T_QTY_INT(), vbExclamation
            Exit Sub
        End If
        If Val(qStr1) <= 0 Then
            MsgBox T_QTY_INT(), vbExclamation
            Exit Sub
        End If
        If Int(Val(qStr1)) <> Val(qStr1) Then
            MsgBox T_QTY_INT(), vbExclamation
            Exit Sub
        End If
        Call SaveWithdrawal(shIn, wkIn, matIn1, CLng(Val(qStr1)))
    Else
        Dim cntM As Integer
        cntM = 0
        Dim sumM As String
        sumM = ""
        Do
            Dim matInM As String
            matInM = InputBox(mLst & Chr(13) & Chr(13) & "#" & (cntM + 1), _
                              T_MULTI_T() & " - " & wkIn)
            If matInM = "" Then Exit Do
            Dim mCM As Long
            mCM = FindMaterialCol(wsSrc, matInM)
            If mCM = -1 Then
                sumM = sumM & "[X] " & matInM & Chr(13)
                GoTo SkipM
            End If
            Dim wRM As Long
            wRM = FindWorkerRow(wsSrc, wkIn)
            Dim curM As String
            curM = Trim(wsSrc.Cells(wRM, mCM).Text)
            Dim qStrM As String
            qStrM = InputBox(matInM & Chr(13) & T_CURR_VAL() & " " & curM & Chr(13) & T_QTY_P(), matInM)
            If qStrM = "" Then GoTo SkipM
            If Not IsNumeric(qStrM) Then
                MsgBox T_QTY_INT(), vbExclamation
                GoTo SkipM
            End If
            If Val(qStrM) <= 0 Or Int(Val(qStrM)) <> Val(qStrM) Then
                MsgBox T_QTY_INT(), vbExclamation
                GoTo SkipM
            End If
            Dim nvM As String
            nvM = AppendNPlus(curM, CLng(Val(qStrM)))
            wsSrc.Cells(wRM, mCM).Value = nvM
            sumM = sumM & "[OK] " & matInM & ": +" & CLng(Val(qStrM)) & " " & T_PCS() & " -> " & nvM & Chr(13)
            cntM = cntM + 1
SkipM:
        Loop
        If cntM > 0 Then
            MsgBox T_MULTI_OK() & "  " & T_SAVED_N() & " " & cntM & Chr(13) & Chr(13) & sumM, vbInformation, T_MULTI_T()
        Else
            MsgBox T_NO_SAVE(), vbInformation
        End If
    End If
    Exit Sub
ErrWW:
    MsgBox T_ERR() & Chr(13) & Err.Description, vbCritical
End Sub

' ===== SaveWithdrawal =====
Sub SaveWithdrawal(shNm As String, wkNm As String, matNm As String, qty As Long)
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo ErrSW
    Dim wsSW As Worksheet
    Set wsSW = ThisWorkbook.Worksheets(shNm)
    Dim wRowSW As Long
    wRowSW = FindWorkerRow(wsSW, wkNm)
    If wRowSW = -1 Then
        MsgBox T_WK_NF(), vbExclamation
        GoTo ClnSW
    End If
    Dim mColSW As Long
    mColSW = FindMaterialCol(wsSW, matNm)
    If mColSW = -1 Then
        MsgBox T_MAT_NF() & " " & matNm, vbExclamation
        GoTo ClnSW
    End If
    Dim curSW As String
    curSW = Trim(wsSW.Cells(wRowSW, mColSW).Text)
    Dim oldN As Long
    oldN = ParseNPlus(curSW)
    Dim newV As String
    newV = AppendNPlus(curSW, qty)
    wsSW.Cells(wRowSW, mColSW).Value = newV
    If SheetExists(SH_FORM2()) Then
        Dim wsFrm As Worksheet
        Set wsFrm = ThisWorkbook.Worksheets(SH_FORM2())
        On Error Resume Next
        wsFrm.Range("D10").Value = IIf(curSW = "", T_EMPTY_V(), curSW) & " (" & T_TOT_PCS() & " " & oldN & ")"
        wsFrm.Range("D11").Value = newV & " (" & T_TOT_PCS() & " " & (oldN + qty) & ")"
        On Error GoTo ErrSW
    End If
    MsgBox T_WD_SAVED() & Chr(13) & Chr(13) & _
           T_WD_SHEET() & ": " & shNm & Chr(13) & _
           T_WD_WK() & ": " & wkNm & Chr(13) & _
           T_WD_MAT() & ": " & matNm & Chr(13) & _
           T_WD_ADD() & ": +" & qty & " " & T_PCS() & Chr(13) & _
           T_WD_OLD() & ": " & IIf(curSW = "", T_EMPTY_V(), curSW) & Chr(13) & _
           T_WD_NEW() & ": " & newV & Chr(13) & _
           T_WD_TOT() & ": " & (oldN + qty) & " " & T_PCS(), _
           vbInformation, T_DONE()
    GoTo ClnSW
ErrSW:
    MsgBox T_ERR() & Chr(13) & Err.Description, vbCritical
ClnSW:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
End Sub

' ===== NewMonthWizard =====
Private Sub NewMonthWizard()
    On Error GoTo ErrNM
    If Not SheetExists(SH_BLANK()) Then
        MsgBox T_TMPL_ERR() & " " & SH_BLANK(), vbCritical
        Exit Sub
    End If
    Dim cntNM As Integer
    cntNM = GetMonthSheetCount()
    Dim nmNM As String
    nmNM = InputBox(T_NEW_SH_T() & Chr(13) & T_NEW_SH_E() & " " & MONTH_PFX() & "3-69" & _
                    Chr(13) & Chr(13) & T_SH_CNT() & " " & cntNM, _
                    T_NEW_SH_T(), MONTH_PFX() & (cntNM + 1) & "-69")
    If nmNM = "" Then Exit Sub
    If SheetExists(nmNM) Then
        MsgBox T_SH_EXIST() & " " & nmNM, vbExclamation
        Exit Sub
    End If
    ThisWorkbook.Worksheets(SH_BLANK()).Copy After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count)
    ActiveSheet.Name = nmNM
    Dim wsNM As Worksheet
    Set wsNM = ActiveSheet
    Dim lrNM As Long
    lrNM = wsNM.Cells(wsNM.Rows.Count, COL_WORKER).End(xlUp).Row
    Dim lcNM As Long
    lcNM = wsNM.Cells(ROW_MAT_HDR, wsNM.Columns.Count).End(xlToLeft).Column
    If lrNM >= 3 And lcNM >= MAT_COL_START Then
        wsNM.Range(wsNM.Cells(3, MAT_COL_START), wsNM.Cells(lrNM, lcNM)).Value = vbNullString
    End If
    MsgBox T_SH_OK() & " " & nmNM & Chr(13) & T_SH_COPY(), vbInformation, T_NEW_SH_T()
    Exit Sub
ErrNM:
    MsgBox T_ERR() & Chr(13) & Err.Description, vbCritical
End Sub

' ===== BuildDashboard2 =====
Sub BuildDashboard2()
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo ErrBD
    If Not SheetExists(SH_DASH2()) Then
        MsgBox T_SH_NF() & " " & SH_DASH2(), vbCritical
        GoTo ClnBD
    End If
    Dim wsDash As Worksheet
    Set wsDash = ThisWorkbook.Worksheets(SH_DASH2())
    Dim msAr As Variant
    msAr = GetMonthSheets()
    If IsEmpty(msAr) Then
        MsgBox T_NO_MNTH(), vbInformation
        GoTo ClnBD
    End If
    Dim matAr As Variant
    matAr = GetMaterials(CStr(msAr(0)))
    If IsEmpty(matAr) Then
        MsgBox T_MAT_NF() & " (empty)", vbInformation
        GoTo ClnBD
    End If
    Dim nM As Integer
    nM = UBound(matAr) + 1
    Dim mi As Integer
    Dim mj As Integer
    Dim rD As Long
    Dim clrE As Long
    clrE = 9 + UBound(msAr) + 2
    If clrE > 9 Then
        wsDash.Range(wsDash.Cells(9, 2), wsDash.Cells(clrE, 2 + nM)).Value = vbNullString
    End If
    For mi = 0 To UBound(msAr)
        Dim wsMo As Worksheet
        Set wsMo = ThisWorkbook.Worksheets(CStr(msAr(mi)))
        Dim lrBD As Long
        lrBD = wsMo.Cells(wsMo.Rows.Count, COL_WORKER).End(xlUp).Row
        Dim dRow As Long
        dRow = 10 + mi
        wsDash.Cells(dRow, 2).Value = CStr(msAr(mi))
        For mj = 0 To nM - 1
            Dim mcBD As Long
            mcBD = FindMaterialCol(wsMo, CStr(matAr(mj)))
            If mcBD > 0 Then
                Dim totBD As Long
                totBD = 0
                For rD = 3 To lrBD
                    totBD = totBD + ParseNPlus(Trim(wsMo.Cells(rD, mcBD).Text))
                Next rD
                wsDash.Cells(dRow, 3 + mj).Value = IIf(totBD > 0, totBD, 0)
            End If
        Next mj
    Next mi
    wsDash.Activate
    MsgBox T_DASH_OK() & Chr(13) & (UBound(msAr) + 1) & " " & MONTH_PFX(), vbInformation, T_DONE()
    GoTo ClnBD
ErrBD:
    MsgBox T_ERR() & Chr(13) & Err.Description & Chr(13) & "Error: " & Err.Number, vbCritical
ClnBD:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
End Sub

' ===== HELPER FUNCTIONS (each name exactly once) =====

Function GetMonthSheetCount() As Integer
    Dim cntG As Integer
    cntG = 0
    Dim wGC As Worksheet
    For Each wGC In ThisWorkbook.Worksheets
        If wGC.Name <> SH_BLANK() And wGC.Name <> SH_FORM2() And wGC.Name <> SH_DASH2() Then
            If Left(wGC.Name, Len(MONTH_PFX())) = MONTH_PFX() Then
                cntG = cntG + 1
            End If
        End If
    Next wGC
    GetMonthSheetCount = cntG
End Function

Function GetMonthSheets() As Variant
    Dim resMS() As Variant
    Dim nMS As Integer
    nMS = 0
    Dim wMS As Worksheet
    For Each wMS In ThisWorkbook.Worksheets
        If wMS.Name <> SH_BLANK() And wMS.Name <> SH_FORM2() And wMS.Name <> SH_DASH2() Then
            If Left(wMS.Name, Len(MONTH_PFX())) = MONTH_PFX() Then
                If nMS = 0 Then
                    ReDim resMS(0)
                Else
                    ReDim Preserve resMS(nMS)
                End If
                resMS(nMS) = wMS.Name
                nMS = nMS + 1
            End If
        End If
    Next wMS
    If nMS = 0 Then
        GetMonthSheets = Empty
    Else
        GetMonthSheets = resMS
    End If
End Function

Function GetWorkers(shGW As String) As Variant
    Dim wsGW As Worksheet
    Set wsGW = ThisWorkbook.Worksheets(shGW)
    Dim lrGW As Long
    lrGW = wsGW.Cells(wsGW.Rows.Count, COL_WORKER).End(xlUp).Row
    Dim resGW() As Variant
    Dim nGW As Integer
    nGW = 0
    Dim rGW As Long
    Dim vGW As String
    For rGW = 3 To lrGW
        vGW = Trim(wsGW.Cells(rGW, COL_WORKER).Text)
        If vGW <> "" And vGW <> "0" And vGW <> "False" Then
            If nGW = 0 Then
                ReDim resGW(0)
            Else
                ReDim Preserve resGW(nGW)
            End If
            resGW(nGW) = vGW
            nGW = nGW + 1
        End If
    Next rGW
    If nGW = 0 Then
        GetWorkers = Empty
    Else
        GetWorkers = resGW
    End If
End Function

Function GetMaterials(shGM As String) As Variant
    Dim wsGM As Worksheet
    Set wsGM = ThisWorkbook.Worksheets(shGM)
    Dim lcGM As Long
    lcGM = wsGM.Cells(ROW_MAT_HDR, wsGM.Columns.Count).End(xlToLeft).Column
    Dim resGM() As Variant
    Dim nGM As Integer
    nGM = 0
    Dim cGM As Long
    Dim vGM As String
    For cGM = MAT_COL_START To lcGM
        vGM = Trim(wsGM.Cells(ROW_MAT_HDR, cGM).Text)
        If vGM <> "" And vGM <> "False" Then
            If nGM = 0 Then
                ReDim resGM(0)
            Else
                ReDim Preserve resGM(nGM)
            End If
            resGM(nGM) = vGM
            nGM = nGM + 1
        End If
    Next cGM
    If nGM = 0 Then
        GetMaterials = Empty
    Else
        GetMaterials = resGM
    End If
End Function

Function ParseNPlus(cTxt As String) As Long
    Dim sPP As String
    sPP = Trim(cTxt)
    If sPP = "" Or sPP = "0" Or sPP = "False" Then
        ParseNPlus = 0
        Exit Function
    End If
    Dim tPP As Long
    tPP = 0
    Dim pArr() As String
    pArr = Split(sPP, "+")
    Dim pIdx As Integer
    Dim pOne As String
    For pIdx = 0 To UBound(pArr)
        pOne = Trim(pArr(pIdx))
        If IsNumeric(pOne) And pOne <> "" Then
            tPP = tPP + CLng(pOne)
        End If
    Next pIdx
    ParseNPlus = tPP
End Function

Function AppendNPlus(eTxt As String, nQty As Long) As String
    If nQty <= 0 Then
        AppendNPlus = Trim(eTxt)
        Exit Function
    End If
    Dim sAP As String
    sAP = Trim(eTxt)
    If sAP = "" Or sAP = "0" Or sAP = "False" Then
        AppendNPlus = CStr(nQty)
        Exit Function
    End If
    Do While Len(sAP) > 0 And Right(sAP, 1) = "+"
        sAP = Left(sAP, Len(sAP) - 1)
    Loop
    AppendNPlus = sAP & "+" & CStr(nQty)
End Function

Function FindWorkerRow(wsFWR As Worksheet, wkFWR As String) As Long
    Dim lrFWR As Long
    lrFWR = wsFWR.Cells(wsFWR.Rows.Count, COL_WORKER).End(xlUp).Row
    Dim rFWR As Long
    For rFWR = 3 To lrFWR
        If Trim(wsFWR.Cells(rFWR, COL_WORKER).Text) = wkFWR Then
            FindWorkerRow = rFWR
            Exit Function
        End If
    Next rFWR
    FindWorkerRow = -1
End Function

Function FindMaterialCol(wsFMC As Worksheet, mNm As String) As Long
    Dim lcFMC As Long
    lcFMC = wsFMC.Cells(ROW_MAT_HDR, wsFMC.Columns.Count).End(xlToLeft).Column
    Dim cFMC As Long
    For cFMC = MAT_COL_START To lcFMC
        If Trim(wsFMC.Cells(ROW_MAT_HDR, cFMC).Text) = mNm Then
            FindMaterialCol = cFMC
            Exit Function
        End If
    Next cFMC
    FindMaterialCol = -1
End Function
