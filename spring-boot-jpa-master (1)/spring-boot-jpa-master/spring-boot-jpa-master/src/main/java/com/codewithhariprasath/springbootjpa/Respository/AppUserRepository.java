package com.codewithhariprasath.springbootjpa.Respository;

import com.codewithhariprasath.springbootjpa.model.AppUser;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

@Repository
public interface AppUserRepository extends JpaRepository<AppUser, Integer> {

    @Query("from AppUser u WHERE u.username=:username AND u.password=:password")
    AppUser findUserByUserNameAndPassword(@Param("username") String username, @Param("password") String password);
}
