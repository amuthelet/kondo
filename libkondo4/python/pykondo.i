%module pykondo
%{
#include "rcb4.h"
#include "ics.h"
%}

int kondo_read_analog(KondoRef ki, int *INOUT, UINT num);
%include "rcb4.h"
%include "ics.h"
