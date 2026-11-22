/* All pairwise products (f)g of the expressions in a file, computed with the
 * original AlChemy reducer under the limits of the runs.  Written by Claude,
 * 21 November 2026; links against lambda.o, utilities.o, conversions.o of the
 * unmodified program.  Mirrors _lambda_action in interact.c: build
 * "eval ((LAW)A)B;", reduce, standardize.  Filters and the copy rule are
 * applied by the caller, on the printed result.
 *
 * usage: products exprs.txt heap_size cycle_limit > products.tsv
 * output: one line per ordered pair, "i<TAB>j<TAB>result", "#" if there is no
 * normal form within the limits or the pair is too long for the buffer. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utilities.h"
#include "include.h"
#include "lambda.h"
#include "conversions.h"

#define LAW "\\f.\\g.(f)g"
#define MAXN 5000

int main (int argc, char **argv)
{
  static char *expr[MAXN];
  static char line[BUFSIZE * 4];
  static char buffer[BUFSIZE];
  int n = 0, i, j;
  FILE *fp;
  interpreter *L;
  parmsLambda *P;
  char *r, *s, *m;

  if (argc != 4) { fprintf (stderr, "usage: products file heap cycles\n"); return 2; }
  fp = fopen (argv[1], "r");
  if (!fp) { perror (argv[1]); return 2; }
  while (n < MAXN && fgets (line, sizeof line, fp))
    {
      line[strcspn (line, "\r\n")] = 0;
      if (!*line) continue;
      expr[n++] = expand_annotation (line);
    }
  fclose (fp);

  P = (parmsLambda *) calloc (1, sizeof (parmsLambda));
  P->heap_size = atoi (argv[2]);
  P->cycle_limit = atoi (argv[3]);
  P->symbol_table_size = 500;
  P->stack_size = 2000;
  P->name_length = 10;
  P->type_length = 100;
  P->standard_variable = 'x';
  P->error_fp = NULL;
  L = initialize_lambda (P);

  for (i = 0; i < n; i++)
    for (j = 0; j < n; j++)
      {
        if (strlen (expr[i]) + strlen (expr[j]) >= BUFSIZE - 500)
          { printf ("%d\t%d\t#\n", i, j); continue; }
        strcpy (buffer, "eval ((");
        strcat (buffer, LAW);
        strcat (buffer, ")");
        strcat (buffer, expr[i]);
        strcat (buffer, ")");
        strcat (buffer, expr[j]);
        strcat (buffer, ";");
        r = reduce_lambda (buffer, L);
        if (!r) { printf ("%d\t%d\t#\n", i, j); continue; }
        s = standardize (r, L);
        free (r);
        if (!s) { printf ("%d\t%d\t#\n", i, j); continue; }
        m = minimize_annotation (s);
        printf ("%d\t%d\t%s\n", i, j, m);
        free (s);
        free (m);
      }
  return 0;
}
