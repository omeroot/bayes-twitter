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
		var counter = 0
		var arr = data[i].split(" ")
		for (var j in arr){
			var subArr = arr[j].split("")
			if (subArr[0] == '@' || isUrl( subArr )){
				counter = 1
				break
			}
		}
		if ( counter == 0)
			words.push(data[i])
	}
	return words	
}

var isUrl = function(word){
	var first4 = [];
	for (var j in word){
		first4.push(word[j])
		if(j == 3)
			break
	}
	if( first4.join("") == "http")
		return true
	else
		return false
}

var splitSubData = function(data,callback){
	var arr = data.replace(/\n/g," ").split(" ")
	callback(null,arr)
}

var splitData = function(data,callback){
	var d = []
	var counter = 0
	if (data.length == 0)
		callback(new Error('data is empty'))
		
	data.forEach(function(element,index,array){
		splitSubData(element,function(err,data){
			d.push(data)
			counter += 1
		});
		if (counter == data.length)
			callback(null,d)
	});
}

fetchTweets('semtinmayoru',400, function (l) {
	var f = fs.createWriteStream(new Date().getTime()+".txt")
	var clear = clearMentionAndUrl(l)
	console.log(clear.length)
	for( var i in clear ){
		f.write(clear[i] + '\n')
	}
	f.end()
	
});