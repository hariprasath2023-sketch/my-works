package com.codewithhariprasath.springbootjpa.Service;

import com.codewithhariprasath.springbootjpa.Respository.AppUserRepository;
import com.codewithhariprasath.springbootjpa.model.AppUser;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Service;

@Service
public class AppUserService {
    @Autowired
    private AppUserRepository appUserRepository;

    public AppUser login(AppUser user) {
        AppUser loggedInUser = appUserRepository
                .findUserByUserNameAndPassword(user.getUsername(), user.getPassword());
        return loggedInUser;
    }

    public AppUser register(AppUser appUser) {
        appUserRepository.save(appUser);
        return appUser;
    }
}
