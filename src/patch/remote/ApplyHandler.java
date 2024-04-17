package emu.lunarcore.server.http.handlers;

import emu.lunarcore.LunarCore;
import emu.lunarcore.game.player.Player;
import emu.lunarcore.server.http.objects.JsonResponse;
import emu.lunarcore.util.Utils;
import io.javalin.http.Context;
import io.javalin.http.Handler;

import org.jetbrains.annotations.NotNull;

import java.util.Random;

public final class ApplyHandler implements Handler {
    @Override
    public void handle(@NotNull Context ctx) throws Exception {
        String ip_address = Utils.getClientIpAddress(ctx);

        var set_uid = ctx.queryParam("uid");

        if (set_uid == null || set_uid.isEmpty()) {
            ctx.json(new JsonResponse(404, "The player UID was not entered"));
            return;
        }


        int tmp_uid = 0;
        try {
            tmp_uid = Integer.parseInt(set_uid);
        } catch (Exception e) {
            ctx.json(new JsonResponse(403, "The UID format is incorrect"));
            return;
        }

        LunarCore.getLogger().info(ip_address + " is applying a tempcode for " + tmp_uid);

        try {
            Player sender = LunarCore.getGameServer().getOnlinePlayerByUid(tmp_uid);

            if (sender != null) {
                sender.sendMessage(ip_address + " is applying a tempcode for you!");

                Random random = new Random();
                int codeInt = 100000 + random.nextInt(900000);
                String codeStr = String.valueOf(codeInt);
                CodeHandler.saveOrUpdateCode(tmp_uid, codeStr);

                sender.sendMessage("Your tempCode is: " + codeStr + " , please quickly verify it!");

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