# python-slack-adapter
## Publish a package

**Test env**
Se publica cada vez que se crea un PR para poder testear el paquete como quedaría. El workflow se hace con las credenciales de @Aliandi. Para cambiarlas hay que eliminar los secrets que existen y volver a crearlos con los nuevos valores. (Esto es Settings->Secrets)

**Prod env**
1. Hay que setear las credenciales de Manx (estan en 1password)
2. Hay que generar un release, para eso primero actualizar la version en el setup.py
3. Listo!
