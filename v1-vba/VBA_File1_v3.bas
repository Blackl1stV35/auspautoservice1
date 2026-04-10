Attribute VB_Name = "Module1"
Option Explicit
'=============================================================================
'  FILE 1 - Purchase Recording System  v3
'  ChrW() only - 100% encoding safe, all codes validated in Thai range 3585-3675
'  Fixes:
'    v3.1: All ChrW codes regenerated from Python ord() - no wrong range codes
'    v3.2: SheetExists confirmed present
'    v3.3: ScreenUpdating + xlCalculationManual in all heavy subs
'    v3.4: ErrH blocks restore both flags
'    v3.5: Full input validation (IsNumeric, IsDate, > 0)
'=============================================================================
' ============ SHEET NAME FUNCTIONS ============
Private Function SH_SI() As String: SH_SI = ChrW(3591) & ChrW(3634) & ChrW(3609) & ChrW(3626) & ChrW(3637): End Function
Private Function SH_KIB() As String: SH_KIB = ChrW(3585) & ChrW(3636) & ChrW(3658) & ChrW(3610) & ChrW(3609) & ChrW(3658) & ChrW(3629) & ChrW(3605): End Function
Private Function SH_OIL() As String: SH_OIL = ChrW(3609) & ChrW(3657) & ChrW(3635) & ChrW(3617) & ChrW(3633) & ChrW(3609): End Function
Private Function SH_LIGHT() As String: SH_LIGHT = ChrW(3627) & ChrW(3621) & ChrW(3629) & ChrW(3604) & ChrW(3652) & ChrW(3615): End Function
Private Function SH_OTHER() As String: SH_OTHER = ChrW(3629) & ChrW(3632) & ChrW(3652) & ChrW(3627) & ChrW(3621) & ChrW(3656) & ChrW(3629) & ChrW(3639) & ChrW(3656) & ChrW(3609) & ChrW(3654): End Function
Private Function SH_SUMMARY() As String: SH_SUMMARY = ChrW(3626) & ChrW(3619) & ChrW(3640) & ChrW(3611) & ChrW(3618) & ChrW(3629) & ChrW(3604) & ChrW(3611) & ChrW(3619) & ChrW(3632) & ChrW(3592) & ChrW(3635) & ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609): End Function
Private Function SH_DASH() As String: SH_DASH = ChrW(3649) & ChrW(3604) & ChrW(3594) & ChrW(3610) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3604): End Function

' ============ CATEGORY LABELS ============
Private Function CAT1() As String: CAT1 = ChrW(3591) & ChrW(3634) & ChrW(3609) & ChrW(3626) & ChrW(3637): End Function
Private Function CAT2() As String: CAT2 = ChrW(3585) & ChrW(3636) & ChrW(3658) & ChrW(3610) & ChrW(3609) & ChrW(3658) & ChrW(3629) & ChrW(3605): End Function
Private Function CAT3() As String: CAT3 = ChrW(3609) & ChrW(3657) & ChrW(3635) & ChrW(3617) & ChrW(3633) & ChrW(3609): End Function
Private Function CAT4() As String: CAT4 = ChrW(3627) & ChrW(3621) & ChrW(3629) & ChrW(3604) & ChrW(3652) & ChrW(3615): End Function
Private Function CAT5() As String: CAT5 = ChrW(3629) & ChrW(3632) & ChrW(3652) & ChrW(3627) & ChrW(3621) & ChrW(3656) & ChrW(3629) & ChrW(3639) & ChrW(3656) & ChrW(3609) & ChrW(3654): End Function

' ============ MONTH NAMES - FIX: all assign to function name ============
Private Function TH_MONTH_NAME(m As Integer) As String
    Select Case m
    Case  1: TH_MONTH_NAME = ChrW(3617) & ChrW(46) & ChrW(3588) & ChrW(46)
    Case  2: TH_MONTH_NAME = ChrW(3585) & ChrW(46) & ChrW(3614) & ChrW(46)
    Case  3: TH_MONTH_NAME = ChrW(3617) & ChrW(3637) & ChrW(46) & ChrW(3588) & ChrW(46)
    Case  4: TH_MONTH_NAME = ChrW(3648) & ChrW(3617) & ChrW(46) & ChrW(3618) & ChrW(46)
    Case  5: TH_MONTH_NAME = ChrW(3614) & ChrW(46) & ChrW(3588) & ChrW(46)
    Case  6: TH_MONTH_NAME = ChrW(3617) & ChrW(3636) & ChrW(46) & ChrW(3618) & ChrW(46)
    Case  7: TH_MONTH_NAME = ChrW(3585) & ChrW(46) & ChrW(3588) & ChrW(46)
    Case  8: TH_MONTH_NAME = ChrW(3626) & ChrW(46) & ChrW(3588) & ChrW(46)
    Case  9: TH_MONTH_NAME = ChrW(3585) & ChrW(46) & ChrW(3618) & ChrW(46)
    Case 10: TH_MONTH_NAME = ChrW(3605) & ChrW(46) & ChrW(3588) & ChrW(46)
    Case 11: TH_MONTH_NAME = ChrW(3614) & ChrW(46) & ChrW(3618) & ChrW(46)
    Case 12: TH_MONTH_NAME = ChrW(3608) & ChrW(46) & ChrW(3588) & ChrW(46)
    End Select
End Function

' ============ UI STRING FUNCTIONS ============
Private Function T_SEL_CAT() As String: T_SEL_CAT = ChrW(3648) & ChrW(3621) & ChrW(3639) & ChrW(3629) & ChrW(3585) & ChrW(3627) & ChrW(3617) & ChrW(3623) & ChrW(3604) & ChrW(3627) & ChrW(3617) & ChrW(3641) & ChrW(3656) & ChrW(32) & ChrW(40) & ChrW(3614) & ChrW(3636) & ChrW(3617) & ChrW(3614) & ChrW(3660) & ChrW(3605) & ChrW(3633) & ChrW(3623) & ChrW(3648) & ChrW(3621) & ChrW(3586) & ChrW(41) & ChrW(58): End Function
Private Function T_CAT_T() As String: T_CAT_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(49) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3627) & ChrW(3617) & ChrW(3623) & ChrW(3604) & ChrW(3627) & ChrW(3617) & ChrW(3641) & ChrW(3656): End Function
Private Function T_SUBTYPE_P() As String: T_SUBTYPE_P = ChrW(3611) & ChrW(3619) & ChrW(3632) & ChrW(3648) & ChrW(3616) & ChrW(3607) & ChrW(3618) & ChrW(3656) & ChrW(3629) & ChrW(3618) & ChrW(32) & ChrW(40) & ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3610) & ChrW(3633) & ChrW(3591) & ChrW(3588) & ChrW(3633) & ChrW(3610) & ChrW(32) & ChrW(3585) & ChrW(3604) & ChrW(32) & ChrW(79) & ChrW(75) & ChrW(32) & ChrW(3648) & ChrW(3614) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3586) & ChrW(3657) & ChrW(3634) & ChrW(3617) & ChrW(41) & ChrW(58): End Function
Private Function T_SUBTYPE_T() As String: T_SUBTYPE_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(50) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3611) & ChrW(3619) & ChrW(3632) & ChrW(3648) & ChrW(3616) & ChrW(3607) & ChrW(3618) & ChrW(3656) & ChrW(3629) & ChrW(3618): End Function
Private Function T_ITEM_P() As String: T_ITEM_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3626) & ChrW(3636) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634) & ChrW(47) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(58): End Function
Private Function T_ITEM_T() As String: T_ITEM_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(51) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3626) & ChrW(3636) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634): End Function
Private Function T_QTY_P() As String: T_QTY_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(58): End Function
Private Function T_QTY_T() As String: T_QTY_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(52) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609): End Function
Private Function T_PRICE_P() As String: T_PRICE_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3619) & ChrW(3634) & ChrW(3588) & ChrW(3634) & ChrW(3605) & ChrW(3656) & ChrW(3629) & ChrW(3594) & ChrW(3636) & ChrW(3657) & ChrW(3609) & ChrW(32) & ChrW(40) & ChrW(3610) & ChrW(3634) & ChrW(3607) & ChrW(44) & ChrW(32) & ChrW(3585) & ChrW(3656) & ChrW(3629) & ChrW(3609) & ChrW(32) & ChrW(86) & ChrW(65) & ChrW(84) & ChrW(41) & ChrW(58): End Function
Private Function T_PRICE_T() As String: T_PRICE_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(53) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3619) & ChrW(3634) & ChrW(3588) & ChrW(3634): End Function
Private Function T_DISC_P() As String: T_DISC_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3626) & ChrW(3656) & ChrW(3623) & ChrW(3609) & ChrW(3621) & ChrW(3604) & ChrW(32) & ChrW(40) & ChrW(48) & ChrW(32) & ChrW(61) & ChrW(32) & ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(3626) & ChrW(3656) & ChrW(3623) & ChrW(3609) & ChrW(3621) & ChrW(3604) & ChrW(41) & ChrW(58): End Function
Private Function T_DISC_T() As String: T_DISC_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(54) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3626) & ChrW(3656) & ChrW(3623) & ChrW(3609) & ChrW(3621) & ChrW(3604): End Function
Private Function T_DISCTYPE_T() As String: T_DISCTYPE_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(54) & ChrW(98) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3619) & ChrW(3641) & ChrW(3611) & ChrW(3649) & ChrW(3610) & ChrW(3610) & ChrW(3626) & ChrW(3656) & ChrW(3623) & ChrW(3609) & ChrW(3621) & ChrW(3604): End Function
Private Function T_VAT_T() As String: T_VAT_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(55) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(86) & ChrW(65) & ChrW(84): End Function
Private Function T_SHOP_P() As String: T_SHOP_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634) & ChrW(47) & ChrW(3612) & ChrW(3641) & ChrW(3657) & ChrW(3592) & ChrW(3633) & ChrW(3604) & ChrW(3592) & ChrW(3635) & ChrW(3627) & ChrW(3609) & ChrW(3656) & ChrW(3634) & ChrW(3618) & ChrW(58): End Function
Private Function T_SHOP_T() As String: T_SHOP_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(56) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634): End Function
Private Function T_DATE_P() As String: T_DATE_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3623) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3595) & ChrW(3639) & ChrW(3657) & ChrW(3629) & ChrW(32) & ChrW(40) & ChrW(3623) & ChrW(3623) & ChrW(47) & ChrW(3604) & ChrW(3604) & ChrW(47) & ChrW(3611) & ChrW(3611) & ChrW(3611) & ChrW(3611) & ChrW(41) & ChrW(58): End Function
Private Function T_DATE_T() As String: T_DATE_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(57) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3623) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656): End Function
Private Function T_BILL_P() As String: T_BILL_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3648) & ChrW(3621) & ChrW(3586) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3610) & ChrW(3636) & ChrW(3621) & ChrW(32) & ChrW(40) & ChrW(3606) & ChrW(3657) & ChrW(3634) & ChrW(3617) & ChrW(3637) & ChrW(41) & ChrW(58): End Function
Private Function T_BILL_T() As String: T_BILL_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(49) & ChrW(48) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3648) & ChrW(3621) & ChrW(3586) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3610) & ChrW(3636) & ChrW(3621): End Function
Private Function T_REM_P() As String: T_REM_P = ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3627) & ChrW(3617) & ChrW(3634) & ChrW(3618) & ChrW(3648) & ChrW(3627) & ChrW(3605) & ChrW(3640) & ChrW(32) & ChrW(40) & ChrW(3606) & ChrW(3657) & ChrW(3634) & ChrW(3617) & ChrW(3637) & ChrW(41) & ChrW(58): End Function
Private Function T_REM_T() As String: T_REM_T = ChrW(3586) & ChrW(3633) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(32) & ChrW(49) & ChrW(49) & ChrW(32) & ChrW(45) & ChrW(32) & ChrW(3627) & ChrW(3617) & ChrW(3634) & ChrW(3618) & ChrW(3648) & ChrW(3627) & ChrW(3605) & ChrW(3640): End Function
Private Function T_CONFIRM_T() As String: T_CONFIRM_T = ChrW(3618) & ChrW(3639) & ChrW(3609) & ChrW(3618) & ChrW(3633) & ChrW(3609) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585): End Function
Private Function T_CONFIRM_Q() As String: T_CONFIRM_Q = ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3609) & ChrW(3637) & ChrW(3657) & ChrW(63): End Function
Private Function T_SAVED_T() As String: T_SAVED_T = ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592): End Function
Private Function T_CAT_L() As String: T_CAT_L = ChrW(3627) & ChrW(3617) & ChrW(3623) & ChrW(3604) & ChrW(3627) & ChrW(3617) & ChrW(3641) & ChrW(3656): End Function
Private Function T_ITEM_L() As String: T_ITEM_L = ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619): End Function
Private Function T_QTY_L() As String: T_QTY_L = ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609): End Function
Private Function T_PRICE_L() As String: T_PRICE_L = ChrW(3619) & ChrW(3634) & ChrW(3588) & ChrW(3634) & ChrW(47) & ChrW(3594) & ChrW(3636) & ChrW(3657) & ChrW(3609): End Function
Private Function T_DISC_L() As String: T_DISC_L = ChrW(3626) & ChrW(3656) & ChrW(3623) & ChrW(3609) & ChrW(3621) & ChrW(3604): End Function
Private Function T_SHOP_L() As String: T_SHOP_L = ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634): End Function
Private Function T_DATE_L() As String: T_DATE_L = ChrW(3623) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656): End Function
Private Function T_TOTAL_L() As String: T_TOTAL_L = ChrW(3618) & ChrW(3629) & ChrW(3604) & ChrW(3619) & ChrW(3623) & ChrW(3617): End Function
Private Function T_BAHT() As String: T_BAHT = ChrW(3610) & ChrW(3634) & ChrW(3607): End Function
Private Function T_YES() As String: T_YES = ChrW(3651) & ChrW(3594) & ChrW(3656): End Function
Private Function T_NO_STR() As String: T_NO_STR = ChrW(3652) & ChrW(3617) & ChrW(3656): End Function
Private Function T_VAT_IN() As String: T_VAT_IN = ChrW(3619) & ChrW(3623) & ChrW(3617) & ChrW(32) & ChrW(86) & ChrW(65) & ChrW(84) & ChrW(32) & ChrW(55) & ChrW(37): End Function
Private Function T_VAT_OUT() As String: T_VAT_OUT = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3617) & ChrW(3637) & ChrW(32) & ChrW(86) & ChrW(65) & ChrW(84): End Function
Private Function T_ERR_CAT() As String: T_ERR_CAT = ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3648) & ChrW(3621) & ChrW(3639) & ChrW(3629) & ChrW(3585) & ChrW(32) & ChrW(49) & ChrW(45) & ChrW(53) & ChrW(32) & ChrW(3648) & ChrW(3607) & ChrW(3656) & ChrW(3634) & ChrW(3609) & ChrW(3633) & ChrW(3657) & ChrW(3609): End Function
Private Function T_ERR_ITEM() As String: T_ERR_ITEM = ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3626) & ChrW(3636) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634): End Function
Private Function T_ERR_QTY() As String: T_ERR_QTY = ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3606) & ChrW(3641) & ChrW(3585) & ChrW(3605) & ChrW(3657) & ChrW(3629) & ChrW(3591): End Function
Private Function T_ERR_PRICE() As String: T_ERR_PRICE = ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3619) & ChrW(3634) & ChrW(3588) & ChrW(3634) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3606) & ChrW(3641) & ChrW(3585) & ChrW(3605) & ChrW(3657) & ChrW(3629) & ChrW(3591): End Function
Private Function T_ERR_SHOP() As String: T_ERR_SHOP = ChrW(3585) & ChrW(3619) & ChrW(3640) & ChrW(3603) & ChrW(3634) & ChrW(3585) & ChrW(3619) & ChrW(3629) & ChrW(3585) & ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634): End Function
Private Function T_ERR_DATE() As String: T_ERR_DATE = ChrW(3619) & ChrW(3641) & ChrW(3611) & ChrW(3649) & ChrW(3610) & ChrW(3610) & ChrW(3623) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3606) & ChrW(3641) & ChrW(3585) & ChrW(3605) & ChrW(3657) & ChrW(3629) & ChrW(3591): End Function
Private Function T_MISS_SH() As String: T_MISS_SH = ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(3614) & ChrW(3610) & ChrW(3594) & ChrW(3637) & ChrW(3605) & ChrW(58): End Function
Private Function T_DASH_OK() As String: T_DASH_OK = ChrW(3619) & ChrW(3637) & ChrW(3648) & ChrW(3615) & ChrW(3619) & ChrW(3594) & ChrW(3649) & ChrW(3604) & ChrW(3594) & ChrW(3610) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3604) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592): End Function
Private Function T_DONE() As String: T_DONE = ChrW(3648) & ChrW(3626) & ChrW(3619) & ChrW(3655) & ChrW(3592) & ChrW(3626) & ChrW(3636) & ChrW(3657) & ChrW(3609): End Function
Private Function T_ERR_DASH() As String: T_ERR_DASH = ChrW(3648) & ChrW(3585) & ChrW(3636) & ChrW(3604) & ChrW(3586) & ChrW(3657) & ChrW(3629) & ChrW(3612) & ChrW(3636) & ChrW(3604) & ChrW(3614) & ChrW(3621) & ChrW(3634) & ChrW(3604) & ChrW(58): End Function
Private Function T_ERR_SAVE() As String: T_ERR_SAVE = ChrW(3648) & ChrW(3585) & ChrW(3636) & ChrW(3604) & ChrW(3586) & ChrW(3657) & ChrW(3629) & ChrW(3612) & ChrW(3636) & ChrW(3604) & ChrW(3614) & ChrW(3621) & ChrW(3634) & ChrW(3604) & ChrW(3586) & ChrW(3603) & ChrW(3632) & ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(58): End Function
Private Function T_MULTI_T() As String: T_MULTI_T = ChrW(3627) & ChrW(3621) & ChrW(3634) & ChrW(3618) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(47) & ChrW(3610) & ChrW(3636) & ChrW(3621): End Function
Private Function T_MULTI_CAT() As String: T_MULTI_CAT = ChrW(3648) & ChrW(3621) & ChrW(3639) & ChrW(3629) & ChrW(3585) & ChrW(3627) & ChrW(3617) & ChrW(3623) & ChrW(3604) & ChrW(3627) & ChrW(3617) & ChrW(3641) & ChrW(3656) & ChrW(3626) & ChrW(3635) & ChrW(3627) & ChrW(3619) & ChrW(3633) & ChrW(3610) & ChrW(3610) & ChrW(3636) & ChrW(3621) & ChrW(3609) & ChrW(3637) & ChrW(3657) & ChrW(58): End Function
Private Function T_MULTI_SHP() As String: T_MULTI_SHP = ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634) & ChrW(32) & ChrW(40) & ChrW(3651) & ChrW(3594) & ChrW(3657) & ChrW(3585) & ChrW(3633) & ChrW(3610) & ChrW(3607) & ChrW(3640) & ChrW(3585) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(41) & ChrW(58): End Function
Private Function T_MULTI_BL() As String: T_MULTI_BL = ChrW(3648) & ChrW(3621) & ChrW(3586) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3610) & ChrW(3636) & ChrW(3621) & ChrW(32) & ChrW(40) & ChrW(3651) & ChrW(3594) & ChrW(3657) & ChrW(3585) & ChrW(3633) & ChrW(3610) & ChrW(3607) & ChrW(3640) & ChrW(3585) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(41) & ChrW(58): End Function
Private Function T_MULTI_VAT() As String: T_MULTI_VAT = ChrW(3588) & ChrW(3636) & ChrW(3604) & ChrW(32) & ChrW(86) & ChrW(65) & ChrW(84) & ChrW(32) & ChrW(55) & ChrW(37) & ChrW(32) & ChrW(3607) & ChrW(3640) & ChrW(3585) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(63) & ChrW(32) & ChrW(32) & ChrW(49) & ChrW(61) & ChrW(3651) & ChrW(3594) & ChrW(3656) & ChrW(32) & ChrW(32) & ChrW(50) & ChrW(61) & ChrW(3652) & ChrW(3617) & ChrW(3656): End Function
Private Function T_MULTI_ITM() As String: T_MULTI_ITM = ChrW(3594) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(32) & ChrW(40) & ChrW(3648) & ChrW(3623) & ChrW(3657) & ChrW(3609) & ChrW(3623) & ChrW(3656) & ChrW(3634) & ChrW(3591) & ChrW(3648) & ChrW(3614) & ChrW(3639) & ChrW(3656) & ChrW(3629) & ChrW(3627) & ChrW(3618) & ChrW(3640) & ChrW(3604) & ChrW(41) & ChrW(58): End Function
Private Function T_MULTI_DONE() As String: T_MULTI_DONE = ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(3626) & ChrW(3635) & ChrW(3648) & ChrW(3619) & ChrW(3655) & ChrW(3592) & ChrW(32) & ChrW(3619) & ChrW(3634) & ChrW(3618) & ChrW(3585) & ChrW(3634) & ChrW(3619) & ChrW(3607) & ChrW(3637) & ChrW(3656) & ChrW(3610) & ChrW(3633) & ChrW(3609) & ChrW(3607) & ChrW(3638) & ChrW(3585) & ChrW(58): End Function
Private Function T_GRAND() As String: T_GRAND = ChrW(3618) & ChrW(3629) & ChrW(3604) & ChrW(3619) & ChrW(3623) & ChrW(3617) & ChrW(3607) & ChrW(3633) & ChrW(3657) & ChrW(3591) & ChrW(3627) & ChrW(3617) & ChrW(3604) & ChrW(58): End Function
Private Function T_TOPSHOP() As String: T_TOPSHOP = ChrW(84) & ChrW(111) & ChrW(112) & ChrW(32) & ChrW(49) & ChrW(48) & ChrW(32) & ChrW(3619) & ChrW(3657) & ChrW(3634) & ChrW(3609) & ChrW(3588) & ChrW(3657) & ChrW(3634) & ChrW(32) & ChrW(3618) & ChrW(3629) & ChrW(3604) & ChrW(3595) & ChrW(3639) & ChrW(3657) & ChrW(3629) & ChrW(3626) & ChrW(3632) & ChrW(3626) & ChrW(3617) & ChrW(3626) & ChrW(3641) & ChrW(3591) & ChrW(3626) & ChrW(3640) & ChrW(3604): End Function
Private Function T_DEUAN() As String: T_DEUAN = ChrW(3648) & ChrW(3604) & ChrW(3639) & ChrW(3629) & ChrW(3609): End Function
Private Function T_KPI_ALL() As String: T_KPI_ALL = ChrW(3605) & ChrW(3657) & ChrW(3609) & ChrW(3607) & ChrW(3640) & ChrW(3609) & ChrW(3619) & ChrW(3623) & ChrW(3617): End Function

Private Function T_DISCTYPE_P() As String
    T_DISCTYPE_P = ChrW(3619) & ChrW(3641) & ChrW(3611) & ChrW(3649) & ChrW(3610) & ChrW(3610) & ChrW(3626) & ChrW(3656) & ChrW(3623) & ChrW(3609) & ChrW(3621) & ChrW(3604) & ChrW(58) & Chr(13) & "1) " & ChrW(3592) & ChrW(3635) & ChrW(3609) & ChrW(3623) & ChrW(3609) & ChrW(3648) & ChrW(3591) & ChrW(3636) & ChrW(3609) & ChrW(32) & ChrW(40) & ChrW(3610) & ChrW(3634) & ChrW(3607) & ChrW(41) & Chr(13) & "2) " & ChrW(3648) & ChrW(3611) & ChrW(3629) & ChrW(3619) & ChrW(3660) & ChrW(3648) & ChrW(3595) & ChrW(3655) & ChrW(3609) & ChrW(3605) & ChrW(3660) & ChrW(32) & ChrW(40) & ChrW(37) & ChrW(41)
End Function

Private Function T_VAT_P() As String
    T_VAT_P = ChrW(3588) & ChrW(3636) & ChrW(3604) & ChrW(32) & ChrW(86) & ChrW(65) & ChrW(84) & ChrW(32) & ChrW(55) & ChrW(37) & ChrW(32) & ChrW(3627) & ChrW(3619) & ChrW(3639) & ChrW(3629) & ChrW(3652) & ChrW(3617) & ChrW(3656) & ChrW(63) & ChrW(32) & ChrW(32) & ChrW(49) & ChrW(61) & ChrW(3651) & ChrW(3594) & ChrW(3656) & ChrW(32) & ChrW(32) & ChrW(32) & ChrW(50) & ChrW(61) & ChrW(3652) & ChrW(3617) & ChrW(3656)
End Function

'=============================================================================
'  ENTRY POINTS  (assign these to buttons)
'=============================================================================
Sub ShowSingleForm():   Call SingleItemWizard: End Sub
Sub ShowMultiForm():    Call MultiItemWizard:  End Sub
Sub RefreshDashboard(): Call BuildDashboard:   End Sub

'=============================================================================
'  SheetExists
'=============================================================================
Function SheetExists(sName As String) As Boolean
    Dim ws As Worksheet
    On Error Resume Next
    Set ws = ThisWorkbook.Worksheets(sName)
    On Error GoTo 0
    SheetExists = Not (ws Is Nothing)
End Function

'=============================================================================
'  BUILD DASHBOARD
'=============================================================================
Sub BuildDashboard()
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo ErrH

    If Not SheetExists(SH_DASH()) Then
        MsgBox T_MISS_SH() & " " & SH_DASH(), vbCritical
        GoTo CleanExit
    End If

    Dim wsD As Worksheet
    Set wsD = ThisWorkbook.Worksheets(SH_DASH())

    Dim shNames(1 To 5) As String
    shNames(1)=SH_SI(): shNames(2)=SH_KIB(): shNames(3)=SH_OIL()
    shNames(4)=SH_LIGHT(): shNames(5)=SH_OTHER()

    Dim dateCols(1 To 5) As Integer
    dateCols(1)=10: dateCols(2)=8: dateCols(3)=8: dateCols(4)=8: dateCols(5)=10

    Dim amtCols(1 To 5) As Integer
    amtCols(1)=8: amtCols(2)=6: amtCols(3)=6: amtCols(4)=6: amtCols(5)=8

    Dim shopCols(1 To 5) As Integer
    shopCols(1)=9: shopCols(2)=7: shopCols(3)=7: shopCols(4)=7: shopCols(5)=9

    Dim aggDict  As Object: Set aggDict  = CreateObject("Scripting.Dictionary")
    Dim shopDict As Object: Set shopDict = CreateObject("Scripting.Dictionary")
    Dim shopCatD As Object: Set shopCatD = CreateObject("Scripting.Dictionary")

    Dim si As Integer, r As Long
    For si = 1 To 5
        If Not SheetExists(shNames(si)) Then GoTo NextSheet
        Dim ws As Worksheet
        Set ws = ThisWorkbook.Worksheets(shNames(si))
        Dim lr As Long: lr = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

        For r = 2 To lr
            Dim dv As Variant: dv = ws.Cells(r, dateCols(si)).Value
            If Not IsDate(dv) Then GoTo NextRow
            Dim dt As Date:       dt    = CDate(dv)
            Dim rawYr As Integer: rawYr = Year(dt)
            Dim beYr As Long
            If rawYr < 2100 Then beYr = rawYr + 600 Else beYr = rawYr
            Dim mo As Integer: mo = Month(dt)

            Dim av As Variant: av = ws.Cells(r, amtCols(si)).Value
            If Not IsNumeric(av) Then GoTo NextRow
            Dim amt As Double: amt = CDbl(av)
            If amt <= 0 Then GoTo NextRow

            Dim k As String: k = beYr & "|" & Format(mo, "00") & "|" & si
            If aggDict.Exists(k) Then
                aggDict(k) = aggDict(k) + amt
            Else
                aggDict.Add k, amt
            End If

            Dim sv As Variant: sv = ws.Cells(r, shopCols(si)).Value
            If IsEmpty(sv) Or sv = "" Then GoTo NextRow
            Dim shop As String: shop = Trim(CStr(sv))
            If Len(shop) < 2 Then GoTo NextRow
            If shopDict.Exists(shop) Then
                shopDict(shop) = shopDict(shop) + amt
            Else
                shopDict.Add shop, amt
                shopCatD.Add shop, shNames(si)
            End If
NextRow:
        Next r
NextSheet:
    Next si

    ' --- Build sorted year-month array ---
    Dim allKeys() As Variant: allKeys = aggDict.Keys
    Dim ymDict As Object: Set ymDict = CreateObject("Scripting.Dictionary")
    Dim i As Integer
    For i = 0 To UBound(allKeys)
        Dim parts() As String: parts = Split(CStr(allKeys(i)), "|")
        Dim ymKey As String: ymKey = parts(0) & "|" & parts(1)
        If Not ymDict.Exists(ymKey) Then ymDict.Add ymKey, 1
    Next i
    Dim ymArr() As String
    ReDim ymArr(0 To ymDict.Count - 1)
    Dim ymKeys() As Variant: ymKeys = ymDict.Keys
    For i = 0 To ymDict.Count - 1: ymArr(i) = CStr(ymKeys(i)): Next i
    Dim j As Integer, tmp As String
    For i = 0 To UBound(ymArr) - 1
        For j = i + 1 To UBound(ymArr)
            If ymArr(j) < ymArr(i) Then
                tmp = ymArr(i): ymArr(i) = ymArr(j): ymArr(j) = tmp
            End If
        Next j
    Next i

    ' --- Write monthly rows starting at row 9 ---
    Const DATA_START As Integer = 9
    Dim dataRow As Integer: dataRow = DATA_START
    Dim grandTotal As Double: grandTotal = 0
    Dim grandBySh(1 To 5) As Double

    For i = 0 To UBound(ymArr)
        Dim ymParts() As String: ymParts = Split(ymArr(i), "|")
        Dim dispYr As Long:    dispYr = CLng(ymParts(0))
        Dim dispMo As Integer: dispMo = CInt(ymParts(1))

        wsD.Cells(dataRow, 2).Value = TH_MONTH_NAME(dispMo) & dispYr

        Dim rowTot As Double: rowTot = 0
        For si = 1 To 5
            Dim kk As String: kk = dispYr & "|" & Format(dispMo, "00") & "|" & si
            Dim cellAmt As Double
            If aggDict.Exists(kk) Then cellAmt = CDbl(aggDict(kk)) Else cellAmt = 0
            If cellAmt > 0 Then
                wsD.Cells(dataRow, 2 + si).Value = cellAmt
                wsD.Cells(dataRow, 2 + si).NumberFormat = "#,##0"
            Else
                wsD.Cells(dataRow, 2 + si).Value = Empty
            End If
            rowTot = rowTot + cellAmt
            grandBySh(si) = grandBySh(si) + cellAmt
        Next si

        If rowTot > 0 Then
            wsD.Cells(dataRow, 8).Value = rowTot
            wsD.Cells(dataRow, 8).NumberFormat = "#,##0"
        Else
            wsD.Cells(dataRow, 8).Value = Empty
        End If
        grandTotal = grandTotal + rowTot

        ' MoM %
        If dataRow > DATA_START Then
            Dim prevTot As Variant: prevTot = wsD.Cells(dataRow - 1, 8).Value
            If IsNumeric(prevTot) And CDbl(prevTot) > 0 And rowTot > 0 Then
                wsD.Cells(dataRow, 9).Value = (rowTot - CDbl(prevTot)) / CDbl(prevTot)
                wsD.Cells(dataRow, 9).NumberFormat = "+0.0%;-0.0%;0%"
            Else
                wsD.Cells(dataRow, 9).Value = Empty
            End If
        End If

        dataRow = dataRow + 1
    Next i

    ' --- KPI cards ---
    wsD.Cells(3, 2).Value = T_KPI_ALL() & Chr(10) & Format(grandTotal, "#,##0") & " " & T_BAHT()
    wsD.Cells(3, 3).Value = CAT1() & Chr(10) & Format(grandBySh(1), "#,##0") & " " & T_BAHT()
    wsD.Cells(3, 5).Value = CAT2() & "+" & CAT3() & Chr(10) & Format(grandBySh(2) + grandBySh(3), "#,##0") & " " & T_BAHT()
    wsD.Cells(3, 6).Value = CAT4() & "+" & CAT5() & Chr(10) & Format(grandBySh(4) + grandBySh(5), "#,##0") & " " & T_BAHT()

    ' --- Top Shops (fixed: rows after chart area = dataRow + 22) ---
    Dim topRow As Integer: topRow = dataRow + 22
    wsD.Cells(topRow, 2).Value = T_TOPSHOP()

    Dim sKeys() As Variant: sKeys = shopDict.Keys
    Dim sVals() As Variant: sVals = shopDict.Items
    Dim n As Integer: n = shopDict.Count
    Dim ii As Integer, jj As Integer
    Dim tmpK As Variant, tmpV As Variant
    For ii = 0 To n - 2
        For jj = ii + 1 To n - 1
            If CDbl(sVals(jj)) > CDbl(sVals(ii)) Then
                tmpV=sVals(ii): sVals(ii)=sVals(jj): sVals(jj)=tmpV
                tmpK=sKeys(ii): sKeys(ii)=sKeys(jj): sKeys(jj)=tmpK
            End If
        Next jj
    Next ii

    Dim topHdr As Integer: topHdr = topRow + 1
    Dim limit As Integer:  limit  = Application.Min(9, n - 1)
    For ii = 0 To limit
        Dim shopRow As Integer: shopRow = topHdr + 1 + ii
        wsD.Cells(shopRow, 2).Value = ii + 1
        wsD.Cells(shopRow, 3).Value = sKeys(ii)
        wsD.Cells(shopRow, 4).Value = shopCatD(sKeys(ii))
        wsD.Cells(shopRow, 5).Value = CDbl(sVals(ii))
        wsD.Cells(shopRow, 5).NumberFormat = "#,##0"
        If grandTotal > 0 Then
            wsD.Cells(shopRow, 6).Value = CDbl(sVals(ii)) / grandTotal
            wsD.Cells(shopRow, 6).NumberFormat = "0.0%"
        End If
    Next ii

    wsD.Activate
    MsgBox T_DASH_OK() & Chr(13) & (UBound(ymArr) + 1) & " " & T_DEUAN(), vbInformation, T_DONE()
    GoTo CleanExit

ErrH:
    MsgBox T_ERR_DASH() & Chr(13) & Err.Description & Chr(13) & "Error: " & Err.Number, vbCritical

CleanExit:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
End Sub

'=============================================================================
'  SINGLE ITEM WIZARD
'=============================================================================
Private Sub SingleItemWizard()
    Dim catMsg As String
    catMsg = T_SEL_CAT() & Chr(13) & Chr(13) & _
             "1) " & CAT1() & Chr(13) & _
             "2) " & CAT2() & Chr(13) & _
             "3) " & CAT3() & Chr(13) & _
             "4) " & CAT4() & Chr(13) & _
             "5) " & CAT5()

    Dim catChoice As String
    catChoice = InputBox(catMsg, T_CAT_T())
    If catChoice = "" Then Exit Sub

    Dim targetSheet As String, catLabel As String
    Select Case Trim(catChoice)
        Case "1": targetSheet = SH_SI():    catLabel = CAT1()
        Case "2": targetSheet = SH_KIB():   catLabel = CAT2()
        Case "3": targetSheet = SH_OIL():   catLabel = CAT3()
        Case "4": targetSheet = SH_LIGHT(): catLabel = CAT4()
        Case "5": targetSheet = SH_OTHER(): catLabel = CAT5()
        Case Else: MsgBox T_ERR_CAT(), vbExclamation: Exit Sub
    End Select

    If Not SheetExists(targetSheet) Then
        MsgBox T_MISS_SH() & " " & targetSheet, vbCritical: Exit Sub
    End If

    Dim subType As String: subType = InputBox(T_SUBTYPE_P(), T_SUBTYPE_T())

    Dim itemName As String
    itemName = InputBox(T_ITEM_P(), T_ITEM_T())
    If Trim(itemName) = "" Then MsgBox T_ERR_ITEM(), vbExclamation: Exit Sub

    Dim qtyStr As String
    qtyStr = InputBox(T_QTY_P(), T_QTY_T())
    If qtyStr = "" Then Exit Sub
    If Not IsNumeric(qtyStr) Then MsgBox T_ERR_QTY(), vbExclamation: Exit Sub
    If Val(qtyStr) <= 0 Then MsgBox T_ERR_QTY(), vbExclamation: Exit Sub

    Dim priceStr As String
    priceStr = InputBox(T_PRICE_P(), T_PRICE_T())
    If priceStr = "" Then Exit Sub
    If Not IsNumeric(priceStr) Then MsgBox T_ERR_PRICE(), vbExclamation: Exit Sub
    If Val(priceStr) <= 0 Then MsgBox T_ERR_PRICE(), vbExclamation: Exit Sub

    Dim discStr As String
    discStr = InputBox(T_DISC_P(), T_DISC_T(), "0")
    If discStr = "" Then discStr = "0"
    If Not IsNumeric(discStr) Or Val(discStr) < 0 Then discStr = "0"

    Dim discType As String: discType = T_BAHT()
    If Val(discStr) > 0 Then
        Dim dtC As String
        dtC = InputBox(T_DISCTYPE_P(), T_DISCTYPE_T(), "1")
        If Trim(dtC) = "2" Then discType = "%"
    End If

    Dim vatC As String
    vatC = InputBox(T_VAT_P(), T_VAT_T(), "1")
    Dim hasVAT As Boolean: hasVAT = (Trim(vatC) = "1")

    Dim shopName As String
    shopName = InputBox(T_SHOP_P(), T_SHOP_T())
    If Trim(shopName) = "" Then MsgBox T_ERR_SHOP(), vbExclamation: Exit Sub

    Dim dateStr As String
    dateStr = InputBox(T_DATE_P(), T_DATE_T(), Format(Date, "dd/mm/yyyy"))
    If dateStr = "" Then Exit Sub
    If Not IsDate(dateStr) Then MsgBox T_ERR_DATE(), vbExclamation: Exit Sub

    Dim billNo As String: billNo = InputBox(T_BILL_P(), T_BILL_T())
    Dim remark As String: remark = InputBox(T_REM_P(),  T_REM_T())

    Dim qty As Double:      qty      = Val(qtyStr)
    Dim price As Double:    price    = Val(priceStr)
    Dim disc As Double:     disc     = Val(discStr)
    Dim subtotal As Double: subtotal = qty * price
    Dim discAmt As Double
    If discType = "%" Then discAmt = subtotal * (disc / 100) Else discAmt = disc
    If discAmt > subtotal Then discAmt = subtotal
    Dim afterDisc As Double: afterDisc = subtotal - discAmt
    Dim vatAmt As Double:    vatAmt    = IIf(hasVAT, afterDisc * 0.07, 0)
    Dim finalAmt As Double:  finalAmt  = afterDisc + vatAmt

    Dim confirmMsg As String
    confirmMsg = "=== " & T_CONFIRM_T() & " ===" & Chr(13) & Chr(13) & _
                 T_CAT_L()   & " : " & catLabel & Chr(13) & _
                 T_ITEM_L()  & " : " & itemName & Chr(13) & _
                 T_QTY_L()   & " : " & qty & Chr(13) & _
                 T_PRICE_L() & " : " & Format(price, "#,##0.00") & " " & T_BAHT() & Chr(13) & _
                 T_DISC_L()  & " : " & disc & " " & discType & Chr(13) & _
                 "VAT 7%"    & "   : " & IIf(hasVAT, T_YES(), T_NO_STR()) & Chr(13) & _
                 T_SHOP_L()  & " : " & shopName & Chr(13) & _
                 T_DATE_L()  & " : " & dateStr & Chr(13) & Chr(13) & _
                 T_TOTAL_L() & " : " & Format(finalAmt, "#,##0.00") & " " & T_BAHT() & Chr(13) & Chr(13) & _
                 T_CONFIRM_Q()

    If MsgBox(confirmMsg, vbYesNo + vbQuestion, T_CONFIRM_T()) = vbNo Then Exit Sub

    Call SaveToSheet(targetSheet, subType, itemName, qty, price, _
                     discAmt, afterDisc, finalAmt, shopName, CDate(dateStr), _
                     billNo, IIf(hasVAT, T_VAT_IN(), T_VAT_OUT()) & IIf(remark = "", "", " | " & remark))
End Sub

'=============================================================================
'  MULTI ITEM WIZARD
'=============================================================================
Private Sub MultiItemWizard()
    On Error GoTo ErrH

    Dim catMsg As String
    catMsg = T_MULTI_CAT() & Chr(13) & Chr(13) & _
             "1) " & CAT1() & "   2) " & CAT2() & "   3) " & CAT3() & _
             "   4) " & CAT4() & "   5) " & CAT5()

    Dim catChoice As String
    catChoice = InputBox(catMsg, T_MULTI_T())
    If catChoice = "" Then Exit Sub

    Dim targetSheet As String, catLabel As String
    Select Case Trim(catChoice)
        Case "1": targetSheet = SH_SI():    catLabel = CAT1()
        Case "2": targetSheet = SH_KIB():   catLabel = CAT2()
        Case "3": targetSheet = SH_OIL():   catLabel = CAT3()
        Case "4": targetSheet = SH_LIGHT(): catLabel = CAT4()
        Case "5": targetSheet = SH_OTHER(): catLabel = CAT5()
        Case Else: MsgBox T_ERR_CAT(), vbExclamation: Exit Sub
    End Select

    If Not SheetExists(targetSheet) Then
        MsgBox T_MISS_SH() & " " & targetSheet, vbCritical: Exit Sub
    End If

    Dim shopName As String: shopName = InputBox(T_MULTI_SHP(), T_MULTI_T())
    If Trim(shopName) = "" Then Exit Sub

    Dim dateStr As String
    dateStr = InputBox(T_DATE_P(), T_DATE_T(), Format(Date, "dd/mm/yyyy"))
    If dateStr = "" Then Exit Sub
    If Not IsDate(dateStr) Then MsgBox T_ERR_DATE(), vbExclamation: Exit Sub

    Dim billNo As String: billNo = InputBox(T_MULTI_BL(),  T_MULTI_T())
    Dim vatC   As String: vatC   = InputBox(T_MULTI_VAT(), T_MULTI_T(), "1")
    Dim hasVAT As Boolean: hasVAT = (Trim(vatC) = "1")

    Dim itemCount As Integer: itemCount = 0
    Dim grandTotal As Double: grandTotal = 0

    Do
        itemCount = itemCount + 1
        Dim itemName As String
        itemName = InputBox(T_MULTI_ITM(), T_MULTI_T() & " #" & itemCount)
        If itemName = "" Then itemCount = itemCount - 1: Exit Do

        Dim qtyStr As String
        qtyStr = InputBox(T_QTY_P(), "#" & itemCount)
        If qtyStr = "" Then GoTo SkipItem
        If Not IsNumeric(qtyStr) Or Val(qtyStr) <= 0 Then
            MsgBox T_ERR_QTY(), vbExclamation: GoTo SkipItem
        End If

        Dim priceStr As String
        priceStr = InputBox(T_PRICE_P(), "#" & itemCount)
        If priceStr = "" Then GoTo SkipItem
        If Not IsNumeric(priceStr) Or Val(priceStr) <= 0 Then
            MsgBox T_ERR_PRICE(), vbExclamation: GoTo SkipItem
        End If

        Dim discStr As String
        discStr = InputBox(T_DISC_P(), "#" & itemCount, "0")
        If Not IsNumeric(discStr) Or Val(discStr) < 0 Then discStr = "0"

        Dim qty As Double:   qty   = Val(qtyStr)
        Dim price As Double: price = Val(priceStr)
        Dim disc As Double:  disc  = Val(discStr)
        Dim sub1 As Double:  sub1  = qty * price
        If disc > sub1 Then disc = sub1
        Dim after As Double: after = sub1 - disc
        Dim fin1 As Double:  fin1  = after + IIf(hasVAT, after * 0.07, 0)
        grandTotal = grandTotal + fin1

        Call SaveToSheet(targetSheet, "", itemName, qty, price, disc, after, fin1, _
                         shopName, CDate(dateStr), billNo, IIf(hasVAT, T_VAT_IN(), T_VAT_OUT()))
SkipItem:
    Loop

    If itemCount > 0 Then
        MsgBox T_MULTI_DONE() & " " & itemCount & Chr(13) & _
               T_GRAND() & " " & Format(grandTotal, "#,##0.00") & " " & T_BAHT(), _
               vbInformation, T_SAVED_T()
    End If
    Exit Sub

ErrH:
    MsgBox T_ERR_SAVE() & Chr(13) & Err.Description, vbCritical
End Sub

'=============================================================================
'  SAVE TO SHEET
'=============================================================================
Private Sub SaveToSheet(sheetName As String, subType As String, itemName As String, _
                         qty As Double, price As Double, discAmt As Double, _
                         afterDisc As Double, finalAmt As Double, shopName As String, _
                         purchDate As Date, billNo As String, remark As String)
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo ErrH

    Dim ws As Worksheet: Set ws = ThisWorkbook.Worksheets(sheetName)
    Dim lr As Long: lr = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row + 1
    If lr < 2 Then lr = 2

    Dim sub1 As Double: sub1 = qty * price
    Dim discPct As String
    If sub1 > 0 And discAmt > 0 Then
        discPct = Format(discAmt / sub1 * 100, "0.00") & "%"
    Else
        discPct = ""
    End If

    Select Case sheetName
        Case SH_SI()
            ws.Cells(lr,1)=subType:   ws.Cells(lr,2)=itemName:  ws.Cells(lr,3)=qty
            ws.Cells(lr,4)=price:     ws.Cells(lr,5)=sub1:      ws.Cells(lr,6)=discPct
            ws.Cells(lr,7)=afterDisc: ws.Cells(lr,8)=finalAmt:  ws.Cells(lr,9)=shopName
            ws.Cells(lr,10)=purchDate: ws.Cells(lr,10).NumberFormat="dd/mm/yyyy"
            ws.Cells(lr,11)=billNo:   ws.Cells(lr,12)=remark
        Case SH_KIB()
            ws.Cells(lr,1)=subType:   ws.Cells(lr,2)=itemName:  ws.Cells(lr,3)=qty
            ws.Cells(lr,4)=price:     ws.Cells(lr,5)=discPct:   ws.Cells(lr,6)=finalAmt
            ws.Cells(lr,7)=shopName
            ws.Cells(lr,8)=purchDate: ws.Cells(lr,8).NumberFormat="dd/mm/yyyy"
            ws.Cells(lr,9)=billNo:    ws.Cells(lr,10)=remark
        Case SH_OIL(), SH_LIGHT()
            ws.Cells(lr,1)=subType:   ws.Cells(lr,2)=itemName:  ws.Cells(lr,3)=qty
            ws.Cells(lr,4)=price:     ws.Cells(lr,5)=discPct:   ws.Cells(lr,6)=finalAmt
            ws.Cells(lr,7)=shopName
            ws.Cells(lr,8)=purchDate: ws.Cells(lr,8).NumberFormat="dd/mm/yyyy"
            ws.Cells(lr,9)=remark
        Case SH_OTHER()
            ws.Cells(lr,1)=subType:   ws.Cells(lr,2)=itemName:  ws.Cells(lr,3)=qty
            ws.Cells(lr,4)=price:     ws.Cells(lr,5)=sub1:      ws.Cells(lr,6)=discPct
            ws.Cells(lr,8)=finalAmt:  ws.Cells(lr,9)=shopName
            ws.Cells(lr,10)=purchDate: ws.Cells(lr,10).NumberFormat="dd/mm/yyyy"
            ws.Cells(lr,11)=billNo:   ws.Cells(lr,12)=remark
    End Select

    Call UpdateMonthlySummary(shopName, finalAmt, purchDate, billNo, remark)

    MsgBox T_SAVED_T() & "!" & Chr(13) & _
           T_ITEM_L() & ": " & itemName & Chr(13) & _
           T_TOTAL_L() & ": " & Format(finalAmt, "#,##0.00") & " " & T_BAHT(), _
           vbInformation, T_SAVED_T()
    GoTo CleanExit

ErrH:
    MsgBox T_ERR_SAVE() & Chr(13) & Err.Description, vbCritical

CleanExit:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
End Sub

'=============================================================================
'  UPDATE MONTHLY SUMMARY
'=============================================================================
Private Sub UpdateMonthlySummary(shopName As String, amount As Double, _
                                   purchDate As Date, billNo As String, remark As String)
    If Not SheetExists(SH_SUMMARY()) Then Exit Sub
    Dim ws As Worksheet: Set ws = ThisWorkbook.Worksheets(SH_SUMMARY())
    Dim lr As Long: lr = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row + 1
    If lr < 2 Then lr = 2
    ws.Cells(lr,1) = purchDate:  ws.Cells(lr,1).NumberFormat = "dd/mm/yyyy"
    ws.Cells(lr,2) = shopName
    ws.Cells(lr,3) = amount:     ws.Cells(lr,3).NumberFormat = "#,##0.00"
    ws.Cells(lr,4) = billNo
    ws.Cells(lr,5) = remark
End Sub

