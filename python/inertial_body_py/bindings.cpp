#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <inertial_body/InertialBody.h>

namespace py = pybind11;
using namespace inertial_body;

PYBIND11_MODULE(inertial_body_py, m) {
    py::class_<InertialBody::InertialState>(m, "State")
        .def_readonly("position", &InertialBody::InertialState::position)
        .def_readonly("velocity", &InertialBody::InertialState::velocity)
        .def_readonly("acceleration", &InertialBody::InertialState::acceleration);

    py::class_<InertialBody>(m, "InertialBody")
        .def(py::init<double, double, double, double>(),
             py::arg("elasticity"),
             py::arg("friction"),
             py::arg("mass"),
             py::arg("distance_exponent"))
        .def("step", &InertialBody::step,
             py::return_value_policy::reference_internal)
        .def("reset", &InertialBody::reset,
             py::arg("pos") = 0.0,
             py::arg("vel") = 0.0)
        .def("set_target", &InertialBody::setTarget)
        .def_property("elasticity",
            &InertialBody::getElasticity,
            &InertialBody::setElasticity)
        .def_property("friction",
            &InertialBody::getFriction,
            &InertialBody::setFriction)
        .def_property("mass",
            &InertialBody::getMass,
            &InertialBody::setMass)
        .def_property("distance_exponent",
            &InertialBody::getDistanceExponent,
            &InertialBody::setDistanceExponent);
}