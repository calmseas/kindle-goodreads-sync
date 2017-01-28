'use strict';

var webpage = require('webpage');
var server = require('webserver').create();
var system = require('system');

var COMMANDS = {
    'createWebPage': createWebPage,
    'getProperty': getProperty,
    'getSetting': getSetting,
    'invokeAsynchronousFunction': invokeAsynchronousFunction,
    'invokeFunction': invokeFunction,
    'setProperty': setProperty,
    'setSetting': setSetting
};

var PAGE_EVENTS = [
    'onAlert',
    'onCallback',
    'onClosing',
    'onConfirm',
    'onConsoleMessage',
    'onError',
    'onFilePicker',
    'onInitialized',
    'onLoadFinished',
    'onLoadStarted',
    'onNavigationRequested',
    'onPageCreated',
    'onPrompt',
    'onResourceError',
    'onResourceReceived',
    'onResourceRequested',
    'onResourceTimeout',
    'onUrlChanged'
];

var PHANTOM_EVENTS = [
    'onError'
];

var counter = 0;

var scopes = {
    'phantom': phantom
};

function emitEvent(event) {
    console.log(JSON.stringify({
        event: event
    }));
}

function execute(command, success, failure) {
    try {
        COMMANDS[command.name].apply(null, [command, success, failure]);
    } catch (error) {
        failure(error);
    }
}

function createWebPage(command, success, failure) {
    var page = webpage.create();
    var uid = counter++;
    PAGE_EVENTS.forEach(function (name) {
        page[name] = function () {
            var args = slice(arguments);
            emitEvent({
                scope: uid,
                name: name,
                args: args
            });
        };
    });
    scopes[uid] = page;
    success({
        uid: uid
    });
}

function getProperty(command, success, failure) {
    var value = scopes[command.scope][command.args[0]];
    success(value);
}

function getSetting(command, success, failure) {
    var value = scopes[command.scope]['settings'][command.args[0]];
    success(value);
}

function invokeAsynchronousFunction(command, success, failure) {
    scopes[command.scope][command.args[0]].apply(scopes[command.scope], command.args[1].concat(success));
}

function invokeFunction(command, success, failure) {
    var value = scopes[command.scope][command.args[0]].apply(scopes[command.scope], command.args[1]);
    success(value);
}

function setProperty(command, success, failure) {
    var value = scopes[command.scope][command.args[0]] = command.args[1];
    success(value);
}

function setSetting(command, success, failure) {
    var value = scopes[command.scope]['settings'][command.args[0]] = command.args[1];
    success(value);
}

function slice(object) {
    return Array.prototype.slice.call(object);
}

PHANTOM_EVENTS.forEach(function (name) {
    phantom[name] = function () {
        var args = slice(arguments);
        emitEvent({
            scope: 'phantom',
            name: name,
            args: args
        });
    };
});

var listening = server.listen(system.args[1], function (request, response) {
    var command;
    if (request.method === 'POST') {
        try {
            command = JSON.parse(request.post);
        } catch (exception) {
            response.statusCode = 400;
            response.write(JSON.stringify(exception));
            response.close();
            return;
        }
        execute(command, function (value) {
            response.statusCode = 200;
            response.write(JSON.stringify(value));
            response.close();
        }, function (error) {
            response.statusCode = 500;
            response.write(JSON.stringify(error));
            response.close();
        });
    } else {
        response.statusCode = 405;
        response.close();
    }
});

console.log(JSON.stringify({
    listening: listening
}));