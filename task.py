import sqlite3 as lite
import datetime


createTable = 'CREATE TABLE IF NOT EXISTS tasks (id, dateStart, dateEnd, task, coment, isActive, isDone, author, authordone );'
insert = 'INSERT INTO tasks(id, dateStart, task, isDone, author, authordone ) VALUES(?, ?, ?, ?, ?, ?);'
try:
   con = lite.connect('task.db')
   cur = con.cursor()

   cur.execute(createTable)
  # cur.execute('INSERT INTO tasks(id) VALUES(?);', (14,))
   
   #data = cur.fetchone()
   #print "SQLite version: %s" % data                
    


   def count(t):
      cur = con.cursor()
      cur.execute('SELECT COUNT(*)+1 FROM tasks;')
      i = cur.fetchone()[0]
      print (i)
      return i

   def getTasks(t):
      print('active tasks:')      
      cur.execute('SELECT id, dateStart, task FROM tasks Where isDone = 0;')
      d = cur.fetchone()
      while d:
         print(d)
         d = cur.fetchone()
      
   def done(t):
      print("done tasks:")
      cur.execute('SELECT id, dateStart, task FROM tasks Where isDone = 1;')
      d = cur.fetchone()
      while d:
         print(d)
         d = cur.fetchone()
   
   
   def createTask(tbl):
      task, = tbl
      time = datetime.datetime.now()
      #cur.execute(insert, (count(), time, task, False, author, doneAuthor))
      cur.execute('INSERT INTO tasks(id, dateStart, task, author, authordone, isDone ) VALUES(?, ?, ?, ?, ?, ?);', (count([]), time, task, "I", "I", 0))
      con.commit()
      #print ("create task called", task, author, doneAuthor)
      return

   def removeId(t):
      id, = t
      cur.execute('delete from tasks where id = :which;', {'which':id})
      con.commit()

   def removeAll(t):
      cur.execute('delete from tasks;')
      con.commit()

   def close():
      con.close()
      print("closed")

   def setDone(t):
      id, = t
      print("id=", id)
      #cur.execute('UPDATE tasks SET dateEnd = ? WHERE id = ?;', (datetime.datetime.now(), id,))
      cur.execute('UPDATE tasks SET isDone = 1 WHERE id = '+id+';');
      #cur.execute('select task from tasks where id = '+id+';')
      #tsk = cur.fetchone()[0]
      #print(tsk)
      #cur.execute('INSERT INTO done_tasks (id, task) values('+id+', "'+tsk+'");')
      con.commit()
      removeId((id,))

   funcs = {'create'   :{'func' : createTask,  'par':['task']},
            'get'      :{'func' : getTasks,    'par':[]},
            'close'    :{'func' : close,       'par':[]},
            'count'    :{'func' : count,       'par':[]},
            'remove'   :{'func' : removeId,    'par':[]},
            'removeAll':{'func' : removeAll,   'par':[]},
            'done'     :{'func' : done,        'par':[]},
            'set'      :{'func' : setDone,     'par':['id']}
            }

   par = []
   com = ""
   
   getTasks([])
   while True:
      command = input("enter command: ");
      if command in funcs:
         tbl = funcs[command]
         params = tbl['par']
         for i in params:
            par.append(input("enter "+i+":"))
         tbl['func'](par)
         par.clear()
      else:
         print("no such command, try this:")
         for i in funcs:
            print('    ',i)

except lite.Error as e:
   print("Error %s:" % e.args[0])
   
    
finally:
   if con:
      con.close()
