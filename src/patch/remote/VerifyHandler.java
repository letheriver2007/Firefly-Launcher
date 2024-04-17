package emu.lunarcore.server.http.handlers;

import emu.lunarcore.LunarCore;
import emu.lunarcore.game.player.Player;
import emu.lunarcore.server.http.objects.JsonResponse;
import emu.lunarcore.util.Utils;
import io.javalin.http.Context;
import io.javalin.http.Handler;

import org.jetbrains.annotations.NotNull;

public final class VerifyHandler implements Handler {
    @Override
    public void handle(@NotNull Context ctx) throws Exception {
        String ip_address = Utils.getClientIpAddress(ctx);

        var set_uid = ctx.queryParam("uid");
        var tmp_code = ctx.queryParam("code");
        var set_password = ctx.queryParam("password");

        if (set_uid == null || set_uid.isEmpty()) {
            ctx.json(new JsonResponse(404, "The player UID was not entered"));
            return;
        }
        if (tmp_code == null || tmp_code.isEmpty()) {
            ctx.json(new JsonResponse(404, "The player password was not entered"));
            return;
        }
        if (set_password == null || set_password.isEmpty()) {
            ctx.json(new JsonResponse(404, "The player remote password was not entered"));
            return;
        }


        int tmp_uid = 0;
        try {
            tmp_uid = Integer.parseInt(set_uid);
        } catch (Exception e) {
            ctx.json(new JsonResponse(403, "The UID format is incorrect"));
            return;
        }

        LunarCore.getLogger().info(ip_address + " is setting remote password for " + tmp_uid);

        try {
            Player sender = LunarCore.getGameServer().getOnlinePlayerByUid(tmp_uid);

            if (sender != null) {
                String code = CodeHandler.getCodeByUid(tmp_uid);

                if (code != null) {
                    if (code.equals(tmp_code)) {
                        sender.sendMessage(ip_address + " is setting your remote password!");
                        PasswordHandler.saveOrUpdatePassword(tmp_uid, set_password);
                        sender.sendMessage("Your remote password is set as : " + set_password);

                    } else {
                        ctx.json(new JsonResponse(201, "The code is incorrect"));
                        return;

                    }

                } else {
                    ctx.json(new JsonResponse(201, "The code is not set"));
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