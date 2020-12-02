##	Project structure
```
deploy/ 
API_project/src/
	:
	| - Fullstack-App
     	| - uservices/
   		| - canteenus 	port=5003 path=/menu/<date:d/m/YEAR>
		| - roomus 	port=5001 path=/room/<id>
		| - secretarius port=5002 path=/secretariat/<Name>/<Local>
		
		

>
> canteenus API returns a dict with 2 keys: lunch(can be a array) and dinner
> 
> *Deploy* code is a submited version but not the final. See the commits 
>
```



### Not implemented. Maybe for future.

```


Ask for a service w/ tokens:
	Example: http://127.0.0.1:5000/api/token/6OAQ29s1fMrKQTVxMg6P

Available services:
hash_services = {
                '6OAQ29s1fMrKQTVxMg6P' : web_pages["room"],
                'YB8rmIMi1qQ33vJlJ5Ik' : web_pages["canteen"],
                'tlDElAgZYbMlppAHwWki' : web_pages["secretariat"],
        }


```
