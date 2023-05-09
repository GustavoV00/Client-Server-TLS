Gustavo Valente Nunes | GRR: 20182557 </br>
Henrique Prokopenko   | GRR: 20186712 </br>

Folder Structure:
    client: Responsible to handle the client </br>
    server: responsible to handle se server </br>
        controllers: Responsible to receive a socket message from client and to respond after. </br>
        service: Controller pass the request to service and do what needs to be done. </br>
        repositories: Operations that services will be used to communicate with database </br>
    db: If needed, configuration file </br>
    log: A Log module </br>
    web: A Report that documents all the project, is a static html page.
