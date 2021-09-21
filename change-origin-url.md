# Cambiar host para pushear con otra cuenta

Como los invite con sus mails de la UM, seguramente no puedan pushear con sus cuentas normales. Entonces pa pushear con sus cuentas de la UM hagan los siguiente:

## Paso 1: Crearse una clave SSH

Vayan a este link y sigan las instrucciones: [Connecting to GitHub with SSH](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

> Si ya tienen una clave SSH para su maquina, cuando esten creandola cambienle el nombre default que les pone.

> Pongan el passphrase vacio

## Paso 2: Clonar el proyecto con SSH

`git clone git@github.com:UM-2021/speech-to-text-app.git`

## Paso 3: Cambiarse el nombre y el mail para commitear en este repo

`git config user.name "su-nombre"`
`git config user.email "su-mail-de-la-um"`

## Paso 4: Agregar el host de github a SSH

Abran el siguiente archivo con algun editor: `~/.ssh/config`

> Por lo general esta ahi, pero vean de abrir el archivo de config de SSH
> Agreguen este host al final del archivo:

```txt
Host github-um
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
```

## Paso 5: Cambiar el remote host del repo

`git remote set-url origin git@github-um:UM-2021/traffic-sign-recognition.git`
