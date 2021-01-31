**CASE:**
***
Automatic backups of the database every 12 hours

**Solution:**
***

1. We select the server we want to make a backup plan. Under maintenance, we found the management option and in there the maintenance plans. With right-click, we create a new maintenance plan. A wiyard pop-up and we follow the steps

![Step_1](./images/manage_backup.png?raw=True)

![Step_2](./task14/images/wizard.png?raw=True)


2. In the following steps, we have only some configurations, names and path selections. We are asked to choose some tasks to be performed during the backup. I go with shrinking the DB, full backup and delete older backup files. In the configuration window, I choose the 12 hours plan.

![properties](./images/properties.png?raw=True)

![tasks](./images/tasks.png?raw=True)

![configurations](./images/configurations.png?raw=True)

![finish](./images/finish.png?raw=True)

3.  After have completed all the steps we are ready to execute our task. Just sit back and enjoy the automatic DB maintance.

![success](./images/success.png?raw=True)

![execute](./images/execute_backup.png?raw=True)



