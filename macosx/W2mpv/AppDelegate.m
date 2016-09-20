//
//  AppDelegate.m
//  W2mpv
//
//  Created by alex on 16/9/18.
//  Copyright © 2016年 alex. All rights reserved.
//

#import "AppDelegate.h"

@interface AppDelegate ()

@property (weak) IBOutlet NSWindow *window;
@end

@implementation AppDelegate

- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
    // Insert code here to initialize your application
}

- (void)applicationWillTerminate:(NSNotification *)aNotification {
    // Insert code here to tear down your application
}

-(void)applicationWillFinishLaunching:(NSNotification *)aNotification
{
    NSAppleEventManager *appleEventManager = [NSAppleEventManager sharedAppleEventManager];
    [appleEventManager setEventHandler:self
                           andSelector:@selector(handleGetURLEvent:withReplyEvent:)
                         forEventClass:kInternetEventClass andEventID:kAEGetURL];
}

- (void)handleGetURLEvent:(NSAppleEventDescriptor *)event withReplyEvent:(NSAppleEventDescriptor *)replyEvent
{
    NSString *path = [[event paramDescriptorForKeyword:keyDirectObject] stringValue];
    [self playInMpv:path];
}

-(void)playInMpv:(NSString *)vodurl {
    NSMutableString *sb = [[NSMutableString alloc] initWithString:vodurl];
    NSString *finalurl = [sb substringFromIndex:6];
    [self exec:@"/usr/local/bin/you-get" setargs:@[@"-p", @"/usr/local/bin/mpv", finalurl] wait:NO];
    
}

-(void)exec:(NSString *)cmd setargs:(NSArray *)args wait:(BOOL) boolvalue {
    
    NSTask *task = [[NSTask alloc] init];
//    task.environment = @{@"PATH":@"/usr/local/bin:/bin:/usr/bin:/usr/sbin:/sbin", @"LC_TYPE":@"zh_CN.UTF-8",@"LANG":@"zh_CN.UTF-8"};
    [task setLaunchPath:cmd];
    [task setArguments:args];
    [task launch];
}

@end
