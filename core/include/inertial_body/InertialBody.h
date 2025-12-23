/*
 * InertialBody.h
 *
 *  Created on: Dec 16, 2025
 *      Author: youngh
 */

#ifndef INERTIALBODY_H_
#define INERTIALBODY_H_

#include <cmath>

namespace inertial_body {

class InertialBody {
 public:
  struct InertialState {
    double target;
    double position;
    double velocity;
    double accelation;

    InertialState(double _target = .0,
                  double _position = .0,
                  double _velocity = .0,
                  double _accelation = .0)
        : target(_target), position(_position), velocity(_velocity), accelation(_accelation) {}
    void reset() {
      target = .0;
      position = .0;
      velocity = .0;
      accelation = .0;
    }
    void step(double _accelation) {
      accelation = _accelation;
      velocity += accelation;
      position += velocity;
    }
    double getDistance() { return target - position; }
  };

  InertialBody(double _elasticity = .5,
               double _friction = .5,
               double _mass = .5,
               double _distanceExponent = 0);

  virtual ~InertialBody();

  void resetMovement();
  InertialState step();

  const InertialState& getCurrentStatus() const;
  double getDistanceExponent() const;
  void setDistanceExponent(double distanceExponent);
  double getElasticity() const;
  void setElasticity(double elasticity);
  double getFriction() const;
  void setFriction(double friction);
  double getMass() const;
  void setMass(double mass);

 private:
  InertialState currentStatus;

  double elasticity;
  double friction;
  double mass;
  double distanceExponent;
};

}  // namespace inertial_body

#endif /* INERTIALBODY_H_ */
