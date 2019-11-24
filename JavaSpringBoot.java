package com.domain.controller;

import com.domain.entity.Users;
import com.domain.entity.UsersList;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.hibernate.engine.jdbc.connections.internal.UserSuppliedConnectionProviderImpl;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.ProtocolException;
import java.net.URL;
import java.util.Collection;
import java.util.List;

//@RestController
//@RequestMapping(value = "http://127.0.0.1:5000/")
//public class Tester {
//    @RequestMapping("/home")
//    public Collection<Users> dodo() {
//        System.out.println();
//
//    }
//}
public class Tester{
    public static void main(String[] args) throws IOException {
        RestTemplate restTemplate = new RestTemplate();
        String fooResourceUrl
                // = "https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=SpringSource";
               = "http://127.0.0.1:5000/home";
        ResponseEntity<String> response
                = restTemplate.getForEntity(fooResourceUrl + "/", String.class);
        //assertThat(response.getStatusCode(), equalTo(HttpStatus.OK));
        String jsonString  = response.getBody() ;
        ObjectMapper mapper = new ObjectMapper();

        List<Users> studentList = (List<Users>) mapper.readValue(jsonString, new TypeReference<List<Users>>(){});
        UsersList list = new UsersList(studentList) ;
        Users user = list.getByIndex(0);
        System.out.println(user.toString());
    }


}