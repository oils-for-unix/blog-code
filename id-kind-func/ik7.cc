#include <cstdint>
#include "stdio.h"

enum class Kind : uint8_t {
  Arith=1, BoolUnary=9, Node=0, KW=2, Lit=12, BoolBinary=13, Op=14, Right=33,
  Left=4, Redir=5, VSub=6, VOp1=32, VTest=34, Assign=129, VOp2=37, Eof=36,
  Ignored=38, Undefined=128, Unknown=130, WS=132, Word=134,
};

enum class Id : uint8_t {
  Arith_Amp=1, Arith_AmpEqual=3, Arith_Bang=5, Arith_Caret=11,
  Arith_CaretEqual=17, Arith_Colon=19, Arith_Comma=21, Arith_DAmp=27,
  Arith_DEqual=33, Arith_DGreat=35, Arith_DGreatEqual=37, Arith_DLess=43,
  Arith_DLessEqual=65, Arith_DMinus=67, Arith_DPipe=69, Arith_DPlus=75,
  Arith_DStar=81, Arith_Equal=83, Arith_Great=85, Arith_GreatEqual=91,
  Arith_LBracket=97, Arith_LParen=99, Arith_Less=101, Arith_LessEqual=107,
  Arith_Minus=129, Arith_MinusEqual=131, Arith_NEqual=133, Arith_Percent=139,
  Arith_PercentEqual=145, Arith_Pipe=147, Arith_PipeEqual=149, Arith_Plus=155,
  Arith_PlusEqual=161, Arith_QMark=163, Arith_RBrace=165, Arith_RBracket=171,
  Arith_RParen=193, Arith_Semi=195, Arith_Slash=197, Arith_SlashEqual=203,
  Arith_Star=225, Arith_StarEqual=227, Arith_Tilde=229,

  BoolUnary_G=9, BoolUnary_L=13, BoolUnary_N=25, BoolUnary_O=29,
  BoolUnary_R=41, BoolUnary_S=45, BoolUnary_a=57, BoolUnary_b=61,
  BoolUnary_c=73, BoolUnary_d=77, BoolUnary_e=89, BoolUnary_f=93,
  BoolUnary_g=105, BoolUnary_h=109, BoolUnary_n=121, BoolUnary_o=125,
  BoolUnary_p=137, BoolUnary_r=141, BoolUnary_s=153, BoolUnary_t=157,
  BoolUnary_u=169, BoolUnary_v=173, BoolUnary_w=185, BoolUnary_x=189,
  BoolUnary_z=201,

  Node_AndOr=0, Node_ArithVar=8, Node_Assign=16, Node_BinaryExpr=24,
  Node_Block=32, Node_Command=40, Node_ConstInt=64, Node_ForEach=72,
  Node_ForExpr=80, Node_Fork=88, Node_FuncCall=96, Node_FuncDef=104,
  Node_NoOp=128, Node_PostDMinus=136, Node_PostDPlus=144, Node_Subshell=152,
  Node_TernaryExpr=160, Node_UnaryExpr=168, Node_UnaryMinus=192,
  Node_UnaryPlus=200,

  KW_Bang=2, KW_Case=10, KW_DLeftBracket=18, KW_Do=26, KW_Done=34, KW_Elif=42,
  KW_Else=66, KW_Esac=74, KW_Fi=82, KW_For=90, KW_Function=98, KW_If=106,
  KW_In=130, KW_Then=138, KW_Until=146, KW_While=154,

  Lit_ArithVarLike=12, Lit_At=28, Lit_Chars=44, Lit_Comma=60,
  Lit_DRightBracket=76, Lit_Digits=92, Lit_EscapedChar=108, Lit_LBrace=124,
  Lit_Other=140, Lit_Percent=156, Lit_Pound=172, Lit_RBrace=188, Lit_Slash=204,
  Lit_Tilde=220, Lit_VarLike=236,

  BoolBinary_DEqual=15, BoolBinary_Equal=31, BoolBinary_EqualTilde=47,
  BoolBinary_NEqual=63, BoolBinary_ef=79, BoolBinary_eq=95, BoolBinary_ge=111,
  BoolBinary_gt=127, BoolBinary_le=143, BoolBinary_lt=159, BoolBinary_ne=175,
  BoolBinary_nt=191, BoolBinary_ot=207,

  Op_Amp=14, Op_DAmp=30, Op_DLeftParen=46, Op_DPipe=62, Op_DRightParen=78,
  Op_DSemi=94, Op_LParen=110, Op_Newline=126, Op_Pipe=142, Op_PipeAmp=158,
  Op_RParen=174, Op_Semi=190,

  Right_ArithSub=49, Right_ArrayLiteral=51, Right_Backtick=53,
  Right_CasePat=59, Right_CommandSub=113, Right_DollarDoubleQuote=115,
  Right_DollarSingleQuote=117, Right_DoubleQuote=123, Right_FuncDef=177,
  Right_SingleQuote=179, Right_Subshell=181, Right_VarSub=187,

  Left_ArithSub=4, Left_ArithSub2=20, Left_Backtick=36, Left_CommandSub=68,
  Left_DollarDoubleQuote=84, Left_DollarSingleQuote=100, Left_DoubleQuote=132,
  Left_ProcSubIn=148, Left_ProcSubOut=164, Left_SingleQuote=196,
  Left_VarSub=228,

  Redir_Clobber=7, Redir_DGreat=23, Redir_DLess=39, Redir_DLessDash=71,
  Redir_Great=87, Redir_GreatAnd=103, Redir_Less=135, Redir_LessAnd=151,
  Redir_LessGreat=167, Redir_TLess=199,

  VSub_Amp=6, VSub_At=22, VSub_Bang=38, VSub_Dollar=70, VSub_Hyphen=86,
  VSub_Name=102, VSub_Number=134, VSub_Pound=150, VSub_QMark=166, VSub_Star=198,

  VOp1_Caret=48, VOp1_Comma=56, VOp1_DCaret=112, VOp1_DComma=120,
  VOp1_DPercent=176, VOp1_DPound=184, VOp1_Percent=240, VOp1_Pound=248,

  VTest_ColonEquals=50, VTest_ColonHyphen=58, VTest_ColonPlus=114,
  VTest_ColonQMark=122, VTest_Equals=178, VTest_Hyphen=186, VTest_Plus=242,
  VTest_QMark=250,

  Assign_Declare=209, Assign_Export=211, Assign_Local=213, Assign_Readonly=219,

  VOp2_Colon=55, VOp2_LBracket=119, VOp2_RBracket=183, VOp2_Slash=247,

  Eof_Backtick=52, Eof_RParen=116, Eof_Real=180,

  Ignored_Comment=54, Ignored_LineCont=118, Ignored_Space=182,

  Undefined_Tok=208,

  Unknown_Tok=210,

  WS_Space=212,

  Word_Compound=214,

};


Kind LookupKind(Id id) {
  int i = static_cast<int>(id);
  int k = 175 & i & ((i ^ 173) + 11);
  return static_cast<Kind>(k);
}

int main() {
  if (LookupKind(Id::Arith_Amp) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_AmpEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Bang) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Caret) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_CaretEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Colon) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Comma) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DAmp) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DGreat) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DGreatEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DLess) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DLessEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DMinus) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DPipe) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DPlus) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_DStar) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Equal) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Great) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_GreatEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_LBracket) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_LParen) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Less) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_LessEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Minus) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_MinusEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_NEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Percent) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_PercentEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Pipe) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_PipeEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Plus) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_PlusEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_QMark) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_RBrace) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_RBracket) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_RParen) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Semi) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Slash) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_SlashEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Star) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_StarEqual) != Kind::Arith) return 1;
  if (LookupKind(Id::Arith_Tilde) != Kind::Arith) return 1;

  if (LookupKind(Id::BoolUnary_G) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_L) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_N) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_O) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_R) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_S) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_a) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_b) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_c) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_d) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_e) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_f) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_g) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_h) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_n) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_o) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_p) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_r) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_s) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_t) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_u) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_v) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_w) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_x) != Kind::BoolUnary) return 1;
  if (LookupKind(Id::BoolUnary_z) != Kind::BoolUnary) return 1;

  if (LookupKind(Id::Node_AndOr) != Kind::Node) return 1;
  if (LookupKind(Id::Node_ArithVar) != Kind::Node) return 1;
  if (LookupKind(Id::Node_Assign) != Kind::Node) return 1;
  if (LookupKind(Id::Node_BinaryExpr) != Kind::Node) return 1;
  if (LookupKind(Id::Node_Block) != Kind::Node) return 1;
  if (LookupKind(Id::Node_Command) != Kind::Node) return 1;
  if (LookupKind(Id::Node_ConstInt) != Kind::Node) return 1;
  if (LookupKind(Id::Node_ForEach) != Kind::Node) return 1;
  if (LookupKind(Id::Node_ForExpr) != Kind::Node) return 1;
  if (LookupKind(Id::Node_Fork) != Kind::Node) return 1;
  if (LookupKind(Id::Node_FuncCall) != Kind::Node) return 1;
  if (LookupKind(Id::Node_FuncDef) != Kind::Node) return 1;
  if (LookupKind(Id::Node_NoOp) != Kind::Node) return 1;
  if (LookupKind(Id::Node_PostDMinus) != Kind::Node) return 1;
  if (LookupKind(Id::Node_PostDPlus) != Kind::Node) return 1;
  if (LookupKind(Id::Node_Subshell) != Kind::Node) return 1;
  if (LookupKind(Id::Node_TernaryExpr) != Kind::Node) return 1;
  if (LookupKind(Id::Node_UnaryExpr) != Kind::Node) return 1;
  if (LookupKind(Id::Node_UnaryMinus) != Kind::Node) return 1;
  if (LookupKind(Id::Node_UnaryPlus) != Kind::Node) return 1;

  if (LookupKind(Id::KW_Bang) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Case) != Kind::KW) return 1;
  if (LookupKind(Id::KW_DLeftBracket) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Do) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Done) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Elif) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Else) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Esac) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Fi) != Kind::KW) return 1;
  if (LookupKind(Id::KW_For) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Function) != Kind::KW) return 1;
  if (LookupKind(Id::KW_If) != Kind::KW) return 1;
  if (LookupKind(Id::KW_In) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Then) != Kind::KW) return 1;
  if (LookupKind(Id::KW_Until) != Kind::KW) return 1;
  if (LookupKind(Id::KW_While) != Kind::KW) return 1;

  if (LookupKind(Id::Lit_ArithVarLike) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_At) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Chars) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Comma) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_DRightBracket) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Digits) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_EscapedChar) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_LBrace) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Other) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Percent) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Pound) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_RBrace) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Slash) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_Tilde) != Kind::Lit) return 1;
  if (LookupKind(Id::Lit_VarLike) != Kind::Lit) return 1;

  if (LookupKind(Id::BoolBinary_DEqual) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_Equal) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_EqualTilde) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_NEqual) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_ef) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_eq) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_ge) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_gt) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_le) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_lt) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_ne) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_nt) != Kind::BoolBinary) return 1;
  if (LookupKind(Id::BoolBinary_ot) != Kind::BoolBinary) return 1;

  if (LookupKind(Id::Op_Amp) != Kind::Op) return 1;
  if (LookupKind(Id::Op_DAmp) != Kind::Op) return 1;
  if (LookupKind(Id::Op_DLeftParen) != Kind::Op) return 1;
  if (LookupKind(Id::Op_DPipe) != Kind::Op) return 1;
  if (LookupKind(Id::Op_DRightParen) != Kind::Op) return 1;
  if (LookupKind(Id::Op_DSemi) != Kind::Op) return 1;
  if (LookupKind(Id::Op_LParen) != Kind::Op) return 1;
  if (LookupKind(Id::Op_Newline) != Kind::Op) return 1;
  if (LookupKind(Id::Op_Pipe) != Kind::Op) return 1;
  if (LookupKind(Id::Op_PipeAmp) != Kind::Op) return 1;
  if (LookupKind(Id::Op_RParen) != Kind::Op) return 1;
  if (LookupKind(Id::Op_Semi) != Kind::Op) return 1;

  if (LookupKind(Id::Right_ArithSub) != Kind::Right) return 1;
  if (LookupKind(Id::Right_ArrayLiteral) != Kind::Right) return 1;
  if (LookupKind(Id::Right_Backtick) != Kind::Right) return 1;
  if (LookupKind(Id::Right_CasePat) != Kind::Right) return 1;
  if (LookupKind(Id::Right_CommandSub) != Kind::Right) return 1;
  if (LookupKind(Id::Right_DollarDoubleQuote) != Kind::Right) return 1;
  if (LookupKind(Id::Right_DollarSingleQuote) != Kind::Right) return 1;
  if (LookupKind(Id::Right_DoubleQuote) != Kind::Right) return 1;
  if (LookupKind(Id::Right_FuncDef) != Kind::Right) return 1;
  if (LookupKind(Id::Right_SingleQuote) != Kind::Right) return 1;
  if (LookupKind(Id::Right_Subshell) != Kind::Right) return 1;
  if (LookupKind(Id::Right_VarSub) != Kind::Right) return 1;

  if (LookupKind(Id::Left_ArithSub) != Kind::Left) return 1;
  if (LookupKind(Id::Left_ArithSub2) != Kind::Left) return 1;
  if (LookupKind(Id::Left_Backtick) != Kind::Left) return 1;
  if (LookupKind(Id::Left_CommandSub) != Kind::Left) return 1;
  if (LookupKind(Id::Left_DollarDoubleQuote) != Kind::Left) return 1;
  if (LookupKind(Id::Left_DollarSingleQuote) != Kind::Left) return 1;
  if (LookupKind(Id::Left_DoubleQuote) != Kind::Left) return 1;
  if (LookupKind(Id::Left_ProcSubIn) != Kind::Left) return 1;
  if (LookupKind(Id::Left_ProcSubOut) != Kind::Left) return 1;
  if (LookupKind(Id::Left_SingleQuote) != Kind::Left) return 1;
  if (LookupKind(Id::Left_VarSub) != Kind::Left) return 1;

  if (LookupKind(Id::Redir_Clobber) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_DGreat) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_DLess) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_DLessDash) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_Great) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_GreatAnd) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_Less) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_LessAnd) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_LessGreat) != Kind::Redir) return 1;
  if (LookupKind(Id::Redir_TLess) != Kind::Redir) return 1;

  if (LookupKind(Id::VSub_Amp) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_At) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Bang) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Dollar) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Hyphen) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Name) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Number) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Pound) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_QMark) != Kind::VSub) return 1;
  if (LookupKind(Id::VSub_Star) != Kind::VSub) return 1;

  if (LookupKind(Id::VOp1_Caret) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_Comma) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_DCaret) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_DComma) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_DPercent) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_DPound) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_Percent) != Kind::VOp1) return 1;
  if (LookupKind(Id::VOp1_Pound) != Kind::VOp1) return 1;

  if (LookupKind(Id::VTest_ColonEquals) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_ColonHyphen) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_ColonPlus) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_ColonQMark) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_Equals) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_Hyphen) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_Plus) != Kind::VTest) return 1;
  if (LookupKind(Id::VTest_QMark) != Kind::VTest) return 1;

  if (LookupKind(Id::Assign_Declare) != Kind::Assign) return 1;
  if (LookupKind(Id::Assign_Export) != Kind::Assign) return 1;
  if (LookupKind(Id::Assign_Local) != Kind::Assign) return 1;
  if (LookupKind(Id::Assign_Readonly) != Kind::Assign) return 1;

  if (LookupKind(Id::VOp2_Colon) != Kind::VOp2) return 1;
  if (LookupKind(Id::VOp2_LBracket) != Kind::VOp2) return 1;
  if (LookupKind(Id::VOp2_RBracket) != Kind::VOp2) return 1;
  if (LookupKind(Id::VOp2_Slash) != Kind::VOp2) return 1;

  if (LookupKind(Id::Eof_Backtick) != Kind::Eof) return 1;
  if (LookupKind(Id::Eof_RParen) != Kind::Eof) return 1;
  if (LookupKind(Id::Eof_Real) != Kind::Eof) return 1;

  if (LookupKind(Id::Ignored_Comment) != Kind::Ignored) return 1;
  if (LookupKind(Id::Ignored_LineCont) != Kind::Ignored) return 1;
  if (LookupKind(Id::Ignored_Space) != Kind::Ignored) return 1;

  if (LookupKind(Id::Undefined_Tok) != Kind::Undefined) return 1;

  if (LookupKind(Id::Unknown_Tok) != Kind::Unknown) return 1;

  if (LookupKind(Id::WS_Space) != Kind::WS) return 1;

  if (LookupKind(Id::Word_Compound) != Kind::Word) return 1;


  printf("PASSED\n");
  return 0;
}
