var Twit = require('twit')
var http = require('http');
var fs = require('fs');
var conf = require('./config')

var download = function(url, dest, cb) {
  var file = fs.createWriteStream(dest);
  http.get(url, function(response) {
    response.pipe(file);
    file.on('finish', function() {
      file.close(cb);  // close() is async, call cb after close completes.
    });
  }).on('error', function(err) { 
    fs.unlink(dest); 
    if (cb) cb(err.message);
  });
};

var client = new Twit({
	consumer_key : conf.consumer_key,
	consumer_secret : conf.consumer_secret,
	access_token : conf.access_token,
	access_token_secret : conf.access_token_secret
});

var fetchImages = function(user){
	client.get("statuses/user_timeline", {
		screen_name: user,
		count: 40
	}, function (err, data, response) {
		data.forEach(function(element,index,array){
			var m = element.entities.media
			if (typeof m != 'undefined'){
				var url = element.entities.media[0].media_url;
				download(url, index + ".jpg",function(err){
					if(err) throw err
				});
			}
		});
	});
}

var fetchTweets = function(user,count, callback){
	var conf = {
		screen_name : user,
		count : count
	}
	var tweets = [ ]
	client.get("statuses/user_timeline", conf, function (err, data, response) {
		for (var i in data){
			tweets.push(data[i].text)
		}
		
		callback(tweets);
	});
}

var clearMentionAndUrl = function(data){
	var words = []
	for (var i in data){
		var arr = data[i].split(" ")
		for (var j in arr){
			var subArr = arr[j].split("")
			if (subArr[0] != '@'){
				words.push(data[i])
				break
			}else{
				break
			}
		}
	}
	return words	
}

fetchTweets('semtinmayoru',20, function (l) {
	console.log(clearMentionAndUrl(l))
});