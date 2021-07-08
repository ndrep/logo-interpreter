from liblet import ANTLR

Logo = ANTLR(
    r"""
	grammar logo;

	prog: (line? EOL)* line?
			;

	line:
		(expression | procedureDeclaration)+
	    ;

    stat: ifStat | ifElseStat | whileStat | repeatStat ;

	ifStat: ('IF' | 'if') (expression | block) block;

	ifElseStat: ('IFELSE' | 'ifelse') (expression | block) block block;

	whileStat: ('WHILE' | 'while') (expression | block) block;

	repeatStat: ('REPEAT' | 'repeat') (expression| block ) block;

	retCmd: stop | output;

cmd:
	fd
	| bk
	| pr
  | lt
	| cs
	| pu
	| pd
	| rw
	| rt
	| ht
	| st
	| home
	| setxy
  | make
  | procedureInvocation
	| sum_
	| modulo
	| int_
  | difference
	| product
	| minus
	| quotient
	| remainder
	| round_
	| sqrt_
  | sin
  | cos
  | radcos
  | arctan
	| power
	| exp
	| log10
	| ln
	| radsin
  | lessequalp
	| greaterequalp
	| random
	| rerandom
	| radarctan
	| lessp
	| greaterp
	| and_
	| or_
	| not_
	| setpos
	| setx
	| sety
	| seth
	| home
	| arc
	| setpencolor
	| setpensize
	| clean
  ;

  addsuboperators: '+'
	  | '-'
	  ;

  muldivoperators: '*'
	  | '/'
	  ;

  compareOperator: '<'
     | '>'
     | '='
     | '>='
     | '<='
	 | '<>'
     ;

  expression: expression EOL*  muldivoperators EOL*   expression
	| expression EOL* addsuboperators EOL* expression
    | ('-' | '+')* '(' expression ')'
	| expression EOL* compareOperator EOL* expression
    | ('-' | '+')* number
    | ('-' | '+')* deref
    | (cmd | retCmd | block | stat | STRINGLITERAL | BOOLEAN )
	;

  pr: ('PRINT' | 'print' | 'PR' | 'pr') EOL* expression
  	| '(' EOL* ('PRINT' | 'print' | 'PR' | 'pr') EOL* (expression) EOL* (expression EOL*)+ ')'
    ;

  rw: ('RW' | 'rw')
  	| ('READWORD' | 'readword')
  	;

  sum_: ('SUM' | 'sum') EOL* expression EOL* expression
  	| '(' EOL* ('SUM' | 'sum')  EOL* expression EOL* expression EOL* (expression EOL*)+  ')'
    ;

  difference: ('DIFFERENCE' | 'difference') EOL* expression EOL* expression;

  quotient: ('QUOTIENT' | 'quotient') EOL* expression EOL* expression
  	| '(' EOL* ('QUOTIENT' | 'quotient') EOL* expression EOL* ')'
    ;

  remainder: ('REMAINDER' | 'remainder') EOL* expression EOL* expression;

  modulo: ('MODULO' | 'modulo') EOL* expression EOL* expression;

  int_: ('INT' | 'int') EOL* expression;

  round_: ('ROUND' | 'round') EOL* expression;

  sqrt_: ('SQRT' | 'sqrt') EOL* expression;

  power: ('POWER' | 'power') EOL* expression EOL* expression;

  exp: ('EXP' | 'exp') EOL* expression;

  log10: ('LOG10' | 'log10') EOL* expression;

  ln: ('LN' | 'ln') EOL* expression;

  sin: ('SIN' | 'sin') EOL* expression;

  radsin: ('RADSIN' | 'radsin') EOL* expression;

  cos: ('COS' | 'cos') EOL* expression;

  radcos: ('RADCOS' | 'radcos') EOL* expression;

  arctan:('ARCTAN' | 'arctan') EOL* expression
  	| '(' EOL* ('ARCTAN' | 'arctan') EOL* expression EOL* expression EOL* ')'
    ;

  radarctan:('RADARCTAN' | 'radarctan') EOL* expression
  	| '(' EOL* ('RADARCTAN' | 'radarctan') EOL* expression EOL* (expression EOL*)+')'
    ;

  product:('PRODUCT' | 'product') EOL* expression EOL* expression
  	| '(' EOL* ('PRODUCT' | 'product') EOL* expression EOL* expression EOL* (expression EOL*)+')'
    ;

  lessp:('LESSP' | 'lessp'| 'LESS?' | 'less?') EOL* expression EOL* expression
      ;

  greaterp:('GREATERP' | 'greaterp' | 'GREATER?' | 'greater?') EOL* expression EOL* expression
      ;

  lessequalp:('LESSEQUALP' | 'lessequalp' | 'LESSEQUAL?' | 'lessequal?') EOL* expression EOL* expression
      ;

  greaterequalp:('GREATEREQUALP' | 'greaterequalp' | 'GREATEREQUAL?' | 'greaterequal?') EOL* expression EOL* expression
      ;

  random:('RANDOM' | 'random') EOL* expression
  	| '(' EOL* ('RANDOM' | 'random') EOL* expression EOL* expression EOL* ')'
    ;

  rerandom:('RERANDOM' | 'rerandom')
      |'(' EOL* ('RERANDOM' | 'rerandom') EOL* expression EOL* ')'
      ;

  and_:('AND' | 'and') EOL* expression EOL* expression
  	| '(' EOL* ('AND' | 'and') EOL* (expression | block) EOL* (expression | block) EOL* (expression | block)+  EOL* ')'
    ;

  or_:('OR' | 'or') EOL* (expression | block) EOL* (expression | block)
  	| '(' EOL* ('OR' | 'or')  EOL* (expression | block) EOL* (expression | block) EOL* (expression | block)+ EOL* ')'
    ;

  not_: ('NOT' | 'not') EOL* (expression | block);

  minus : ('MINUS' | 'minus')  EOL* expression;

  fd: ('FD' | 'fd' | 'FORWARD' | 'forward')  EOL* expression;

  bk: ('BK' | 'bk' | 'BACK' | 'back')  EOL* expression;

  lt: ('LT' | 'lt' | 'LEFT' | 'left')  EOL* expression;

  rt: ('RT' | 'rt' | 'RIGHT' | 'right')  EOL* expression;

  setpos: ('SETPOS' | 'setpos')  EOL* expression  EOL* expression;

  setxy: ('SETXY' | 'setxy')  EOL* expression  EOL* expression;

  setx: ('SETX' | 'setx')  EOL* expression;

  sety: ('SETY' | 'sety')  EOL* expression;

  seth: ('SETH' | 'seth' | 'SETHEADING' | 'setheading')  EOL* expression;

  home: ('HOME' | 'home');

  arc: ('ARC' | 'arc')  EOL* expression  EOL* expression;

  st: ('ST' | 'st' | 'SHOWTURTLE' | 'showturtle');

  ht: ('HT' | 'ht' | 'HIDETURTLE' | 'hideturtle');

  clean: ('CLEAN' | 'clean');

  cs: ('CS' | 'cs' | 'CLEARSCREEN' | 'clearscreen');

  setpensize: ('SETPENSIZE' | 'setpensize')  EOL* expression;

  setpencolor: ('SETPENCOLOR' | 'setpencolor' | 'SETPC' | 'setpc')  EOL* colorBlock;

  pu: ('PU' | 'pu' | 'PENUP' | 'penup');

  pd: ('PD' | 'pd' | 'PENDOWN' | 'pendown');

  make: ('MAKE' | 'make') EOL* (STRINGLITERAL | deref)  EOL* expression;

  deref: ( ':' | 'THING' | 'thing' )  (name | STRINGLITERAL | deref);

  parameterDeclarations: ':' name (',' parameterDeclarations)*;

  procedureDeclaration:
  	('TO' | 'to') name  parameterDeclarations* EOL? ((line)? EOL)+ ('END' | 'end');

	parameters: expression
    ;

  procedureInvocation: name parameters
  	| '(' name ')'
	| '(' name parameters parameters+ ')'
    ;

  stop: ('STOP' | 'stop');

  output: ('OUTPUT' | 'output' | 'OP' | 'op')  EOL* expression ;

  block: '[' EOL* ((expression ) EOL* )+ EOL* ']';

  colorBlock: '[' EOL* ((expression ) EOL* )+ EOL* ']';

  number: NUMBER;

  name: STRING ;

  BOOLEAN: '"'?(T R U E | F A L S E);

    fragment A: [aA];
    fragment E: [eE];
    fragment F: [fF];
    fragment L: [lL];
    fragment R: [rR];
    fragment S: [sS];
    fragment T: [tT];
    fragment U: [uU];


 STRINGLITERAL: '"' STRING
     ;

  STRING: [a-zA-Z] [a-zA-Z0-9_]*;

  NUMBER: '.'? [0-9]+ '.'? [0-9]?;

  EOL: '\r'? '\n';

  WS: [ \t\r\n] -> skip;

"""
)
