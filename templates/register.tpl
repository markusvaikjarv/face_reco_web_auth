<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>👁 Registreeri</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css">
    <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
</head>

<body>

    <div class="container is-fluid">
        <h1 class="has-text-centered is-size-3">Registreeri</h1>
        <form action="/registerupload" method="post" enctype="multipart/form-data">
            <input class="input is-rounded" required="true" type="text" placeholder="Kasutajanimi" name="kasutajanimi" />
            <input class="input is-rounded" placeholder="Parool" type="password" required="true" name="parool" />
            <div class="container has-text-centered">
                <button id="kaameranupp" class="button is-danger kaamera-button" onclick="take_picture()"><i class="fas fa-video kaamera-ikoon"></i>Käivita
                    kaamera</button>
            </div>
            <div class="container has-text-centered">
                <div class="upload-btn-wrapper">
                    <button class="filebtn"><i class="far fa-image kaamera-ikoon"></i>Vali pilt</button>
                    <input accept="image/jpeg" required="true" type="file" name="upload" />
                </div>
            </div>
            <div class="container has-text-centered">
                <input type="submit" class="button is-primary" value="Registreeri" />
            </div>

        </form>
    </div>
    <video id="vid"></video>
    <style>
        .upload-btn-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
        }

        .kaamera-ikoon {
            margin-right: 10px;
        }

        .is-danger {
            margin-top: 5px;
        }

        .is-fluid {
            margin-top: 20px;
        }

        .filebtn {
            margin-top: 5px;
            border: 2px solid gray;
            color: black;
            background-color: white;
            padding: 8px 20px;
            border-radius: 2.5px;
            font-size: 14px;

        }

        .upload-btn-wrapper input[type=file] {
            font-size: 100px;
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
        }
    </style>
    <script>
        (() => {if(performance.navigation.type == 2){
            location.reload(true);
        }})() //vajalik selleks, et "tagasi" nuppu vajutades form puhas oleks

        const isOpera = (!!window.opr && !!opr.addons) || !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
        const isChrome = !!window.chrome && !!window.chrome.webstore;
        const isBlink = (isChrome || isOpera) && !!window.CSS;


        function take_picture() {
// Kui leht on productionis siis viskab errori kui SSL ceri pole ja klient kasutab Chrome
//        if (location.protocol !== 'https:') {
//            if (isBlink) {alert("Kasutad Chromel põhinevat brauserit. Kuna veebilehel puudub SSL cert ei tööta ka veebikaamera funktsionaalsus. Proovi kasutada FireFoxi.")}
//        }
            document.getElementById("kaameranupp").innerText = "Salvesta pilt"
            const vid = document.querySelector('video');
            vid.style.display = "none"
            navigator.mediaDevices.getUserMedia({
                    video: true
                }) // kysime kasutajalt kaamera jaoks luba
                .then(stream => {
                    vid.srcObject = stream; 
                    return vid.play(); 
                })
                .then(() => { 
                    const btn = document.querySelector('button');
                    btn.disabled = false;
                    btn.onclick = e => {
                        takeASnap()
                            .then(download);
                    };
                })
                .catch(e => console.log(e));

            function takeASnap() {
                const canvas = document.createElement('canvas'); 
                canvas.style.display = "none"
                const ctx = canvas.getContext('2d'); 
                canvas.width = vid.videoWidth; 
                canvas.height = vid.videoHeight;
                ctx.drawImage(vid, 0, 0); 
                return new Promise((res, rej) => {
                    canvas.toBlob(res, 'image/jpeg'); 
                });
            }

            function download(blob) {
                let a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = 'screenshot.jpg';
                document.body.appendChild(a);
                a.click();
            }


        }
    </script>

</body>

</html>