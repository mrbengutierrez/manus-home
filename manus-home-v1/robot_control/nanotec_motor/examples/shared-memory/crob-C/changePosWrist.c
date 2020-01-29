// getpos - example progam using the shared memory api
// to retrieve position and velocity from the control loop

// make sure you run "go" to load control loop first!

// run make to make getpos (see ./Makefile)

#include "/opt/the77lab/robot/crob/ruser.h"
#include "/opt/the77lab/robot/crob/rtl_inc.h"
// robot decls
#include "/opt/the77lab/robot/crob/robdecls.h"

// pointers to shared buffer objects
main()
{
  s32 ob_shmid;
  Ob *ob;

  ob_shmid = shmget(OB_KEY, sizeof(Ob), IPC_CREAT | 0666);
  ob = shmat(ob_shmid, NULL, 0);
  memset( ob, 0, sizeof(Ob) );
  
	double aa = 0.0, fe = 0.0, ps = 0.0;
  printf("a +0.1 to aa, b -0.1 to aa, f +0.1 to fe, e -0.1 to fe\n");
  printf("p +0.1 to ps, s -0.1 to ps, i to init all to 0, q to quit\n");
  char c = 'c';
  while ( c != 'q' )
  {
    printf("aa: %f, fe: %f, ps: %f\n", ob->wrist.pos.aa, ob->wrist.pos.fe, ob->wrist.pos.ps );
    c = getchar();
    switch ( c )
		{
      case 'a':
        aa += 0.1;
        break;
      case 'b':
        aa -= 0.1;
        break;
      case 'f':
        fe += 0.1;
        break;
      case 'e':
        fe -= 0.1;
        break;
      case 'p':
        ps += 0.1;
        break;
      case 's':
        ps -= 0.1;
        break;
      case 'i':
        aa = 0.0;
        fe = 0.0;
        ps = 0.0;
        break;
		}
    ob->wrist.pos.aa = aa;
    ob->wrist.pos.fe = fe;
    ob->wrist.pos.ps = ps;
  }

  shmdt(ob);
}
