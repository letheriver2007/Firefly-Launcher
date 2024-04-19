package emu.lunarcore.server.http.handlers;

import emu.lunarcore.LunarCore;
import emu.lunarcore.game.player.Player;
import emu.lunarcore.server.http.objects.JsonResponse;
import emu.lunarcore.util.Utils;
import io.javalin.http.Context;
import io.javalin.http.Handler;

import org.jetbrains.annotations.NotNull;

public final class RemoteHandler implements Handler {
    @Override
    public void handle(@NotNull Context ctx) throws Exception {
        String ip_address = Utils.getClientIpAddress(ctx);

        var set_uid = ctx.queryParam("uid");
        var key = ctx.queryParam("key");
        var command = ctx.queryParam("command");

        if (set_uid == null || set_uid.isEmpty()) {
            ctx.json(new JsonResponse(404, "The player UID was not entered"));
            return;
        }

        if (key == null || key.isEmpty()) {
            ctx.json(new JsonResponse(404, "The password was not entered"));
            return;
        }
        if (command == null || command.isEmpty()) {
            ctx.json(new JsonResponse(404, "The command was not entered"));
            return;
        }

        int tmp_uid = 0;
        try {
            tmp_uid = Integer.parseInt(set_uid);
        } catch (Exception e) {
            ctx.json(new JsonResponse(403, "The UID format is incorrect"));
            return;
        }

        LunarCore.getLogger().info(ip_address + " execute the command " + command + " remotely to " + tmp_uid);

        try {
            Player sender = LunarCore.getGameServer().getOnlinePlayerByUid(tmp_uid);

            if (sender != null) {
                String pwd = PasswordHandler.getPasswordByUid(tmp_uid);
                String encrypted_key = PasswordHandler.hashWithMD5(key);

                if (pwd != null) {
                    if (pwd.equals(encrypted_key)){
                        sender.sendMessage(ip_address + " use execute the command " + command + " remotely to you");
                        LunarCore.getCommandManager().invoke(sender, command);

                    } else {
                        ctx.json(new JsonResponse(201, "The key is incorrect"));
                        return;
                    }

                } else {
                    ctx.json(new JsonResponse(201, "The key is not set"));
                    return;

                }

            } else {
                ctx.json(new JsonResponse(201, "The player is not online"));
                return;

            }

        } catch (Exception e) {
            LunarCore.getLogger().info("error", e);
            ctx.json(new JsonResponse(403, "error"));
            return;
        }


        ctx.json(new JsonResponse());
    }
}