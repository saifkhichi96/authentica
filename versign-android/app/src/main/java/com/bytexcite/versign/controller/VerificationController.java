package com.bytexcite.versign.controller;

import android.util.Log;

import com.bytexcite.versign.model.entity.SignatureImage;
import com.bytexcite.versign.model.entity.VerificationRequest;
import com.bytexcite.versign.model.entity.VerificationResponse;
import com.bytexcite.versign.util.WebServer;

import java.net.MalformedURLException;

import sfllhkhan95.android.rest.HttpMethod;
import sfllhkhan95.android.rest.HttpRequest;


/**
 * VerificationController allows sending a VerificationRequest to the web server and receiving
 * an VerificationResponse in response.
 *
 * @author saifkhichi96
 * @version 1.0
 * @see VerificationRequest
 * @see VerificationResponse
 */
public class VerificationController {

    private WebServer server = new WebServer();

    public VerificationController() throws MalformedURLException {
    }

    public HttpRequest<VerificationResponse> getVerificationRequest(
            String customerID, SignatureImage signatureImage) {
        return new VerifyRequest(new VerificationRequest(customerID, signatureImage));
    }

    private class VerifyRequest extends HttpRequest<VerificationResponse> {

        VerifyRequest(VerificationRequest request) {
            super(server, "src/controller/VerificationController.php", VerificationResponse.class);
            setMethod(HttpMethod.POST);
            setPayload(request);
        }

        @Override
        protected void onExecuteFailed(Exception ex) {
            ex.printStackTrace();
            Log.e("DroidREST", ex.getMessage());
        }
    }
}