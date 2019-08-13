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
    ob->wrist.pos.aa = 0.0;
    ob->wrist.pos.fe = 0.0;
    ob->wrist.pos.ps = 0.0;
    shmdt(ob);
}
