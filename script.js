import responseJson from '/songs/spotifyReleases.json' assert {type: 'json'};

var path = window.location.pathname;
var page = path.split("/").pop();

function onWindowLoad() {
    BonusReleases();

    if (page == "index" || page == "" || page == "index.html") {
        getLatestRelease();
    } else if (page == "library" || page == "ibrary.html") {
        getAllReleases();
    }

}

function getLatestRelease() {
    const latestRelease = responseJson.items[0];

    document.getElementById("latestReleaseLink").href = `songs/-${latestRelease.name}`;
    document.getElementById("latestReleaseName").textContent = latestRelease.name;
    document.getElementById("latestReleaseImg").src = latestRelease.images[0].url;
    document.getElementById("latestEmb").src = `https://open.spotify.com/embed/album/${latestRelease.id}?utm_source=generator`;

}

var bonusList = [];

function getAllReleases() {
    let itemsPerRows = 3; // Handles how many items per row

    // Handles the releases from Spotify
    let s = "<tr>";
    for (let i = 0; i < responseJson.items.length; i++) {
        if (i % itemsPerRows == 0 && i != 0) {
            s += "</tr><tr>"
        }
        s += `<td><h3 style='font - size: 20px; margin: 10px'> ${responseJson.items[i].name} </h3>`;

        s += `<a href='songs/-${responseJson.items[i].name}'><img src='${responseJson.items[i].images[0].url}' width=275px /></a>`;
    }

    document.getElementById("discography").insertAdjacentHTML("beforeend", s);
    // -------
    // Handles the bonus releases
    let b = "<tr>";
    for (let i = 0; i < bonusList.length; i++) {
        if (i % itemsPerRows == 0 && i != 0) {
            b += "</tr><tr>";
        }
        b += `<td><h3 style='font - size: 20px; margin: 10px'> ${bonusList[i].displayName}</h3>`;
        b += `<a href='${bonusList[i].url}' target='_blank'><img src='${bonusList[i].img}' width=275px /></a>`;
    }

    document.getElementById("bonus").insertAdjacentHTML("beforeend", b);

}


function BonusReleases() { // Put specific tracks here
    let twilightReverbed = new BonusTrack("twilight (slowed + reverbed) (YT only)", "eH3cU5dr2f4");



}


function Teaser() {
    let active = false; // Set to false to disable entire catagory
    //-----------------
    // Change parameters of the teaser track
    const teaser = {
        displayName: "",
        releaseDate: "",
        img: ""
    }

    if (active) {
        let s = "";
        s += '<div class="content">'
        s += '<h3 style="font-size: 35px; margin: 10px">Coming soon . . . </h3>'
        s += `<h3 style="font-size: 30px; margin: 10px">${teaser.displayName}</h3>`;
        s += `<img src="${teaser.img}" width=350px />`;
        s += `<p>${teaser.releaseDate}</p>`;
        s += '</div>'

        document.getElementById("teaser").insertAdjacentHTML("beforeend", s);
    }

}

class BonusTrack {
    // Constructor for YouTube-only release
    constructor(displayName, ytID) {
        this.displayName = displayName;
        this.ytID = ytID;
        this.url = `https://www.youtube.com/watch?v=${ytID}`;
        this.img = `https://img.youtube.com/vi/${ytID}/0.jpg`;
        bonusList.push(this);
    }
}

onWindowLoad();